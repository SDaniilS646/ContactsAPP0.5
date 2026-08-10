from django.utils import timezone

from .company_service import CompanyService
from .contact_service import ContactService
from .employees_service import EmployeeService
from .material_service import MaterialService
from .meeting_service import MeetingService

from .connection_service import ConnectionService



class PageService:
  @staticmethod
  def contacts_page():
    contacts = ContactService.get_contacts()
    contacts = contacts.order_by('last_name')
    loaded_contacts = []
  
    for cont in contacts:
      loaded_contacts.append({
        'id': cont.id,
        'name': f'{cont.last_name} {cont.first_name} {cont.patronymic}',
        'phone': cont.phone,
        'mail': cont.mail,
        'comment':cont.comment,
        'is_old': True if (timezone.now().date() - cont.updated_at.date()).days > 365 else False,
        'updated_at': cont.updated_at
      })

    return 'contacts/contacts_page.html', {'contacts':loaded_contacts}

  @staticmethod
  def companies_page():

    companies = CompanyService.get_companies()
    companies = companies.order_by('id')
    
    loaded_companies = []
  
    for comp in companies:
      loaded_companies.append({
        'id': comp.id,
        'name': comp.name,
        'inn': comp.inn,
        'phone': comp.phone,
        'mail': comp.mail,
        'comment': comp.comment,
        'materials': ' '.join([item.name for item in comp.materials.all()]),
        'is_old': True if (timezone.now().date() - comp.updated_at.date()).days > 365 else False,
        'updated_at': comp.updated_at
      })

    return 'companies/companies_page.html', {'companies':loaded_companies} 

  @staticmethod
  def materials_page():
    materials = MaterialService.get_materials()

    material_tree = MaterialService.get_material_tree()

    return 'materials/materials_page.html', {'materials':materials, 'material_tree': material_tree}

  @staticmethod
  def employees_page():
    employees = EmployeeService.get_employees()
    employees = employees.order_by('last_name')

    return 'employees/employees_page.html', {
      'employees':employees, 
      'style': 'cards'
    }

  @staticmethod
  def meetings_page():
    meetings = MeetingService.get_meetings()
    loaded_meetings = []

    for meeting in meetings:
      contacts = meeting.contacts.all()
      employees = meeting.employees.all()
      companies = meeting.companies.all()

      loaded_meetings.append({
        'id': meeting.id,
        'subject': meeting.subject,
        'meeting_date': meeting.meeting_date,
        'employees': ', '.join([employee.last_name for employee in employees]),
        'contacts': ', '.join([contact.last_name for contact in contacts]),
        'companies': ', '.join([company.name for company in companies])
      })



    return 'meetings/meetings_page.html', {'meetings':loaded_meetings}

  @staticmethod
  def cmd_page():
    return 'commands/commands_page.html', {}

class DetailService:
  @staticmethod
  def companiesDetail(company_id):
    company = CompanyService.get_company(company_id)
    
    comp_cont = ConnectionService.get_company_contact('company', company_id)
  
    contacts = company.contacts.all()
    cont_info = []
  
    materials = None
    materials = company.materials.all()
  
    for cont in contacts:
      temp_info = [item for item in comp_cont if item.contact_id == cont.id]
      cont_info.append({
        'contact_id': cont.id,
        'cont_name': f'{cont.last_name} {cont.first_name}',
        'position': temp_info[0].position,
        'phone': temp_info[0].phone,
        'mail':temp_info[0].mail
      })
  
    rating = company.rating
    if company.rating:
      rating = '★' * int(company.rating)

    return 'companies/detail.html', {'company':company,
      'cont_info': cont_info,
      'materials': materials,
      'rating': rating, 
      }

  @staticmethod
  def contactsDetail(id):
    contact = ContactService.get_contact(id)
    comp_cont = ConnectionService.get_company_contact('contact', id)
  
    companies = contact.companies.all()
  
    comp_info = []
  
    for company in companies:
      temp_info = [item for item in comp_cont if item.company_id == company.id]
      comp_info.append({
        'company_id': company.id,
        'company_name': company.name,
        'position': temp_info[0].position,
        'phone': temp_info[0].phone,
        'mail':temp_info[0].mail
      })

    return 'contacts/detail.html', {'contact':contact,'comp_info':comp_info}

  @staticmethod
  def materialsDetail(id):
    material = MaterialService.get_material(id)
    # material_tree = MaterialService.get_material_tree()
  
    materials = MaterialService.get_materials()
  
    parent = None
    children = None
    companies = None
  
    if material.parent_id:
      parent = MaterialService.get_parent(material.parent_id)
  
    children = MaterialService.get_children(id)
    companies = material.companies.all()
  
    all_children = MaterialService.getAllChildren(id, materials)

    return 'materials/detail.html', {
          'this_material':material,
          'parent': parent,
          'children': children,
          'companies': companies,
          # 'material_tree': material_tree,
          'all_children': all_children
        }

  @staticmethod
  def meetingsDetail(id):
    meeting = MeetingService.get_meeting(id)
    
    contacts = meeting.contacts.all()
    employees = meeting.employees.all()
    companies = meeting.companies.all()

    return 'meetings/detail.html', {
          'meeting':meeting,
          'contacts': contacts,
          'employees': employees,
          'companies': companies
        }

class AddService:

  @staticmethod
  def addCompanyPage():
    return 'companies/add_comp.html', {}

  @staticmethod
  def addMeetingPage():
    return 'meetings/add_meeting.html', {}

class ModalService:
  @staticmethod
  def createMaterial(id):
    material_tree = MaterialService.get_material_tree()

    return 'components/modal_create_material.html', {'material_tree': material_tree}

  @staticmethod
  def createContact(id):
    return 'components/modal_create_contact.html', {}

  @staticmethod
  def createEmployee(id):
    return 'components/modal_create_employee.html', {}

  @staticmethod
  def chooseMaterial(company_id):
    """

    Строит иерархическое дерево материалов.

    :param old_mats: id материалов, которые нужно пометить как выбранные (selected=True)

    :return: список корневых узлов дерева, каждый узел содержит вложенные children

    """
    template = 'components/modal_choose_material.html'
    if not company_id:
      material_tree = MaterialService.get_material_tree()
      return template, {'material_tree': material_tree}

    company = CompanyService.get_company(company_id)
  
    comp_mat_ids = list(company.materials.values_list('id', flat=True))

    material_tree = MaterialService.get_material_tree(old_mats=comp_mat_ids)

    return template, {'material_tree': material_tree, 'company_id':company_id}

  @staticmethod
  def chooseCompany(meeting_id):
    template = 'components/modal_choose_company.html'

    if not meeting_id:
      companies = CompanyService.get_companies()
      return template, {'companies': companies}

  @staticmethod
  def chooseContact(company_id):
    """

    Готовит контекст для модалки выбора контакта.

    Если company_id не передан — возвращает список всех контактов без выделения.

    Если передан — помечает selected=True для контактов, привязанных к компании,

    и добавляет корпоративные данные (mail, phone, position), сортируя выбранные наверх.

    """

    template = 'components/modal_choose_contact.html'
    all_contacts = ContactService.get_contacts()

    contacts_list = [
      {
        'id': contact.id,
        'cont_name': ' '.join(filter(None, [contact.last_name, contact.first_name, contact.patronymic])),
        'phone': contact.phone,
        'mail': contact.mail,
        'selected': False,
        'corp_mail': None,
        'corp_phone': None,
        'position': None
      }
      for contact in all_contacts
    ]

    if not company_id:
      return template, {'contacts': contacts_list}

    company_contacts_connection = ConnectionService.get_company_contact('company', company_id)

    company_contacts = {item.contact_id: item for item in company_contacts_connection}
            
    for contact in contacts_list:
      
      if contact['id'] in company_contacts:
        connection = company_contacts[contact['id']]

        contact.update({
          'selected': True,
          'corp_mail': connection.mail,
          'corp_phone': connection.phone,
          'position': connection.position
        })

    contacts_list.sort(key=lambda contact: contact['selected'], reverse=True)

    return template, {'contacts': contacts_list, 'company_id':company_id}
    
  @staticmethod
  def chooseEmployee(id):
    employees = EmployeeService.get_employees()
    return 'components/modal_choose_employees.html', {'employees': employees}

  @staticmethod
  def editCompany(id):
    company = CompanyService.get_company(id)
    return 'components/modal_edit_company.html', {'company':company}

  @staticmethod
  def editContact(id):
    contact = ContactService.get_contact(id)
    return 'components/modal_edit_contact.html', {'contact':contact}

  @staticmethod
  def editMaterial(material_id):
    material = MaterialService.get_material(material_id)
    
    materials = MaterialService.get_materials()
    material_tree = MaterialService.get_material_tree(materials=materials)

    parent = MaterialService.get_parent(material.parent_id) if material.parent_id else None
    
    children = [m for m in materials if m.parent_id == material.id]
    companies = material.companies.all()
  
    all_children = MaterialService.getAllChildren(material_id, materials)

    return 'components/modal_edit_material.html', {
      'this_material':material,
      'parent': parent,
      'children': children,
      'companies': companies,
      'material_tree': material_tree,
      'all_children': all_children
    }

  @staticmethod
  def editEmployee(id):
    employee = EmployeeService.get_employee(id)
    return 'components/modal_edit_employee.html', {'employee': employee}