from django.utils import timezone
from django.db.models import F

from apps.crm.services.model_services.company_service import CompanyService
from apps.crm.services.model_services.contact_service import ContactService
from apps.crm.services.model_services.employees_service import EmployeeService
from apps.crm.services.model_services.material_service import MaterialService, MeasureService
from apps.crm.services.model_services.meeting_service import MeetingService
from apps.crm.services.model_services.object_service import ObjectService

from apps.crm.services.model_services.connection_service import ConnectionService

from apps.sender.sender_services import get_version

from apps.sender.models import TrainingExample

from apps.ai.services.ai_services import AiService



class PageService:
  @staticmethod
  def sender_page():
    model_version = f'work_classifier {get_version("work_classifier")}'
    return 'sender/sender_page.html', {'model_version': model_version}

  @staticmethod
  def ai_config_page():
    model_list = AiService.get_ai_models()
    return 'ai/ai_page.html', {'model_list': model_list}
  
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
        'is_old': True if comp.updated_at and ( timezone.now().date() - comp.updated_at.date()).days > 365 else False,
        'updated_at': comp.updated_at
      })

    return 'companies/companies_page.html', {'companies':loaded_companies} 

  @staticmethod
  def materials_page():
    materials = MaterialService.get_materials()
    materials = materials.order_by('name')
    material_tree = MaterialService.get_material_tree(materials=materials)
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
  def objects_page():
    objects = ObjectService.get_objects()
    return 'objects/objects_page.html', {'objects': objects}

  @staticmethod
  def cmd_page():
    return 'commands/commands_page.html', {}

  @staticmethod
  def parser_page():
    return 'companies/parse_comp_page.html', {}

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
  def objectsDetail(id):
    
    object = ObjectService.get_object(id)
    brend_list = ConnectionService.get_brend_list(id)


    sections = [brend.section for brend in brend_list]
    sections = list(set(sections))

    sections = [{'name':section, 'value':section.replace(' ', '_')} for section in sections]

    frame = [
      {
        'name':section['name'],
        'value':section['value'],
        'categories': []
      }
      for section in sections
    ]

    for item in brend_list:
      item.section = item.section.replace(' ', '_')

    for section in frame:
      categories = []

      temp_categories = [
        {
          'name': item.material.parent.name,
          'id': item.material.parent.id
        }
        for item in brend_list
        if item.section == section['value']
      ]

      for category in temp_categories:
        if category not in categories:
          categories.append(category)

      section['categories'] = [
        {
          'id': category['id'],
          'name': category['name'],
          'materials': [
            {
              'id': material.id,
              'name': material.name,
              'brends':  [
                {
                  'name': brend.company.name,
                  'id': brend.company.id
                }
                for brend in brend_list
                if brend.section == section['value']
                and brend.material.id == material.id
              ]
            }
            for material in {
              item.material.id: item.material
              for item in brend_list
              if item.section == section['value']
              and item.material.parent.id == category['id']
            }.values()
          ]
        }
        for category in categories
      ]


    return 'objects/detail.html', {'object': object, 'sections': sections, 'frame':frame}

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
      'material':material,
      'parent': parent,
      'children': children,
      'companies': companies,
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

  @staticmethod
  def modelDetail(id):
    model = AiService.get_ai_model(id)
    model_versions = AiService.get_ai_versions(model)
    active_version = model_versions.filter(is_active=True).first().id

    return 'ai/detail.html', {'model':model, 'versions':model_versions, 'active_version':active_version}

class AddService:

  @staticmethod
  def addCompanyPage():
    return 'companies/add_comp.html', {}

  @staticmethod
  def addMeetingPage():
    return 'meetings/add_meeting.html', {}

class ModalService:
  modal_template = 'components/modals'
  @staticmethod
  def listMeasure(id):
    measures = MeasureService.get_measures()
    measures = measures.order_by('name')
    return ModalService.modal_template + '/modal_list_measure.html', {'measures': measures}

  @staticmethod
  def createMaterial(id):
    material_tree = MaterialService.get_material_tree()
    measures = MeasureService.get_measures()
    measures = measures.order_by('name')
    return ModalService.modal_template + '/create/modal_create_material.html', {'material_tree': material_tree, 'measures': measures}

  @staticmethod
  def createMeasure(id):
    return ModalService.modal_template + '/create/modal_create_measure.html', {}

  @staticmethod
  def createContact(id):

    return ModalService.modal_template + '/create/modal_create_contact.html', {'company_id':id if id else ''}

  @staticmethod
  def createEmployee(id):
    return ModalService.modal_template + '/create/modal_create_employee.html', {}

  @staticmethod
  def createObject(id):
    return ModalService.modal_template + '/create/modal_create_object.html', {}

  @staticmethod
  def createModel(id):
    task = AiService.get_ai_model(id)
    model = AiService.get_last_version(task)
    return ModalService.modal_template + '/create/modal_create_aiversion.html', {'model':model}

  @staticmethod
  def chooseMaterial(company_id):
    template = ModalService.modal_template + '/choose/modal_choose_material.html'
    if not company_id:
      material_tree = MaterialService.get_material_tree()
      return template, {'material_tree': material_tree}

    company = CompanyService.get_company(company_id)
  
    comp_mat_ids = list(company.materials.values_list('id', flat=True))

    material_tree = MaterialService.get_material_tree(old_mats=comp_mat_ids)

    return template, {'material_tree': material_tree, 'company_id':company_id}

  @staticmethod
  def chooseCompany(meeting_id):
    template = ModalService.modal_template + '/choose/modal_choose_company.html'

    if not meeting_id:
      companies = CompanyService.get_companies()
      return template, {'companies': companies}

  @staticmethod
  def chooseContact(company_id):
    template = ModalService.modal_template + '/choose/modal_choose_contact.html'
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
    return ModalService.modal_template + '/choose/modal_choose_employees.html', {'employees': employees}

  @staticmethod
  def chooseBrendList(id):
    total_companies = CompanyService.get_companies()
    object = ObjectService.get_object(id)
    selected = ConnectionService.get_brend_list(id)

    selected_brends = []
    selected_materials = []
    for brend in selected:
      selected_brends.append(brend.company.id)
      selected_materials.append(f'{brend.company.id}_{brend.material.id}')

    companies = []
    for company in total_companies:
      materials = company.materials.all()
      temp = {
        'id': company.id,
        'name': company.name,
        'materials': [{
          'id':material.id,
          'name':material.name,
          'parent': material.parent.name if material.parent else None,
          'section': MaterialService.get_section(material).name if MaterialService.get_section(material) else None,
          'selected':'selected' if f'{company.id}_{material.id}' in selected_materials else ''} for material in materials
        ],
        'selected': 'selected-parent' if company.id in selected_brends else ''
      }

      companies.append(temp)
    return ModalService.modal_template + '/choose/modal_choose_brendlist.html', {'companies': companies, 'object': object}
  
  @staticmethod
  def editCompany(id):
    company = CompanyService.get_company(id)
    return ModalService.modal_template + '/edit/modal_edit_company.html', {'company':company}

  @staticmethod
  def editContact(id):
    contact = ContactService.get_contact(id)
    return ModalService.modal_template + '/edit/modal_edit_contact.html', {'contact':contact}

  @staticmethod
  def editMaterial(material_id):
    template = ModalService.modal_template + '/edit/modal_edit_material.html'
    material = MaterialService.get_material(material_id)
    
    materials = MaterialService.get_materials()
    materials = materials.order_by('name')
    material_tree = MaterialService.get_material_tree(materials=materials)

    parent = MaterialService.get_parent(material.parent.id) if material.parent else None
    
    children = [m for m in materials if m.parent == material.id]
    companies = material.companies.all()
  
    all_children = MaterialService.getAllChildren(material_id, materials)

    measures = MeasureService.get_measures()

    return template, {
      'material':material,
      'measures': measures,
      'parent': parent,
      # 'children': children,
      # 'companies': companies,
      'material_tree': material_tree,
      'all_children': all_children
    }

  @staticmethod
  def editMeasure(id):
    measure = MeasureService.get_measure(id)
    return ModalService.modal_template + '/edit/modal_edit_measure.html', {'measure': measure}

  @staticmethod
  def editEmployee(id):
    employee = EmployeeService.get_employee(id)
    return ModalService.modal_template + '/edit/modal_edit_employee.html', {'employee': employee}

  @staticmethod
  def editObject(id):
    object = ObjectService.get_object(id)
    return ModalService.modal_template + '/edit/modal_edit_object.html', {'object': object}


  @staticmethod
  def alCategories(id):
    
    pending = TrainingExample.objects.filter(status='pending').annotate(
      percentage=F("uncertainity_score") * 100
    )

    categories = TrainingExample.objects.filter(label__isnull=False, status__in=['labeled', 'reviewed'])
    unique_categories = list(set([cat.label for cat in categories]))

    pending_count = len(pending)

    return ModalService.modal_template + '/ml/modal_categories_al.html', {'pending': pending, 'categories':unique_categories, 'pending_count': pending_count}