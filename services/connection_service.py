from apps.connections.models import CompanyContact, CompanyMaterial, MeetingContact, MeetingEmployee, MeetingCompany
from services.company_service import CompanyService
from services.material_service import MaterialService
from services.contact_service import ContactService
from services.meeting_service import MeetingService
from services.employees_service import EmployeeService

from django.utils import timezone

class ConnectionService:
  @staticmethod
  def set_company_contact(input_data):
    new_id = CompanyContact.objects.create(
      company = CompanyService.get_company(input_data['comp_id']),
      contact = ContactService.get_contact(input_data['cont_id']),
      position = input_data['cont_position'],
      mail = input_data['cont_mail'],
      phone = input_data['cont_phone'],
      added_at = timezone.now()
    )

    return new_id
  
  @staticmethod
  def set_company_material(input_data):
    new_id = CompanyMaterial.objects.create(
      company = CompanyService.get_company(input_data['comp_id']),
      material = MaterialService.get_material(input_data['mat_id']),
      is_main = None,
      added_at = timezone.now()
    )
    return new_id
  
  @staticmethod
  def get_company_contact(column, id, id_2=None):
    if column == 'contact':
      return CompanyContact.objects.filter(contact=id)
    elif column == 'company':
      return CompanyContact.objects.filter(company=id)
    elif column == 'company_contact':
      return CompanyContact.objects.filter(company=id, contact=id_2)

  @staticmethod
  def get_companies_contacts(all_company_ids):
    return CompanyContact.objects.filter(company_id__in=all_company_ids)
    
  @staticmethod
  def get_company_material(column, id):
    if column == 'material':
      return CompanyMaterial.objects.filter(material=id)
    elif column == 'company':
      return CompanyMaterial.objects.filter(company=id)
    
  @staticmethod
  def delete_material_connection(comp_id, mat_id):
    id = CompanyMaterial.objects.get(company=comp_id, material=mat_id).id
    CompanyMaterial.objects.filter(id=id).delete()
  
  @staticmethod
  def delete_contact_connection(comp_id, cont_id):
    id = CompanyContact.objects.get(company=comp_id, contact=cont_id).id
    CompanyContact.objects.filter(id=id).delete()
    
  @staticmethod
  def edit_company_contact(input_data):
    CompanyContact.objects.create(
      company = CompanyService.get_company(input_data['comp_id']),
      contact = ContactService.get_contact(input_data['cont_id']),
      position = input_data['cont_position'],
      mail = input_data['cont_mail'],
      phone = input_data['cont_phone'],
      added_at = timezone.now()
    )

  @staticmethod
  def edit_company_material(input_data):
    CompanyMaterial.objects.create(
      company = CompanyService.get_company(input_data['comp_id']),
      material = MaterialService.get_material(input_data['mat_id']),
      is_main = None,
      added_at = timezone.now()
    )

  @staticmethod
  def set_meeting_contact(input_data):
    new_id = MeetingContact.objects.create(
      meeting = MeetingService.get_meeting(input_data['meet_id']),
      contact = ContactService.get_contact(input_data['cont_id']),
      added_at = timezone.now()
    )
    return new_id
  
  @staticmethod
  def set_meeting_employee(input_data):
    new_id = MeetingEmployee.objects.create(
      meeting = MeetingService.get_meeting(input_data['meet_id']),
      emloyee = EmployeeService.get_employee(input_data['emp_id']),
      added_at = timezone.now()
    )
    return new_id

  @staticmethod
  def set_meeting_company(input_data):
    new_id = MeetingCompany.objects.create(
      meeting = MeetingService.get_meeting(input_data['meet_id']),
      company = CompanyService.get_company(input_data['company_id']),
      # added_at = timezone.now()
    )
    return new_id

  @staticmethod
  def delete_all_contact_connections(comp_id):
    CompanyContact.objects.filter(company=comp_id).delete()

  @staticmethod
  def delete_all_material_connections(comp_id):
    CompanyMaterial.objects.filter(company=comp_id).delete()