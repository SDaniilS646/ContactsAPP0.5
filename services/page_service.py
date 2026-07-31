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
        'first_name': cont.first_name,
        'last_name': cont.last_name,
        'patronymic': cont.patronymic,
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

    return 'meetings/meetings_page.html', {'meetings':meetings}

class DetailService:
  @staticmethod
  def companiesDetail(id):
    company = CompanyService.get_company(id)
    
    comp_cont = ConnectionService.get_company_contact('company', id)
    comp_cont_ids = [item.contact_id for item in comp_cont]
  
    contacts = company.contacts.all()
    cont_info = []
  
    materials = None
    materials = company.materials.all()
  
    comp_mat_ids = [item.id for item in materials]
  
    material_tree = MaterialService.get_material_tree(comp_mat_ids)
    all_contacts = ContactService.get_contacts()
  
    contacts_list = []
  
    for cont in all_contacts:
      if cont.id in comp_cont_ids:
        temp = [{'corp_mail': item.mail, 'corp_phone': item.phone, 'position': item.position} for item in comp_cont if item.contact_id == cont.id][0]
        contacts_list.append({
          'id': cont.id,
          'first_name': cont.first_name,
          'last_name': cont.last_name,
          'patronymic': cont.patronymic,
          'phone': cont.phone,
          'mail': cont.mail,
          'selected': True,
          'corp_mail': temp['corp_mail'],
          'corp_phone': temp['corp_phone'],
          'position': temp['position']
        })
      else:
        contacts_list.append({
          'id': cont.id,
          'first_name': cont.first_name,
          'last_name': cont.last_name,
          'patronymic': cont.patronymic,
          'phone': cont.phone,
          'mail': cont.mail
        })
  
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
          'material_tree': material_tree,
          'contacts': contacts_list}

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
    material_tree = MaterialService.get_material_tree()
  
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
          'material_tree': material_tree,
          'all_children': all_children
        }

  @staticmethod
  def employeesDetail(id):
    employee = EmployeeService.get_employee(id)
    emp_info = []

    return 'employees/detail.html', {
      'employee':employee,
      'emp_info':emp_info
    }

  @staticmethod
  def meetingsDetail(id):
    meeting = MeetingService.get_meeting(id)
    
    contacts = meeting.contacts.all()
    employees = meeting.employees.all()

    return 'meetings/detail.html', {
          'meeting':meeting,
          'contacts': contacts,
          'employees': employees
        }


class AddService:

  @staticmethod
  def addCompanyPage():
    material_tree = MaterialService.get_material_tree()
    contacts = ContactService.get_contacts()

    return 'companies/add_comp.html', {'material_tree': material_tree,'contacts': contacts}

class ModalService:
  @staticmethod
  def createMaterial():
    material_tree = MaterialService.get_material_tree()

    return 'components/modal_create_material.html', {'material_tree': material_tree}

  @staticmethod
  def createContact():
    return 'components/modal_create_contact.html', {}

  @staticmethod
  def createEmployee():
    return 'components/modal_create_employee.html', {}

  @staticmethod
  def chooseMaterial():
    material_tree = MaterialService.get_material_tree()
    return 'components/modal_choose_material.html', {'material_tree': material_tree}

  @staticmethod
  def chooseContact():
    contacts = ContactService.get_contacts()
    return 'components/modal_choose_contact.html', {'contacts': contacts}