from apps.crm.models.connections import CompanyContact, CompanyMaterial, MeetingContact, MeetingEmployee, MeetingCompany
from .model_services.company_service import CompanyService
from .model_services.material_service import MaterialService
from .model_services.contact_service import ContactService
from .model_services.meeting_service import MeetingService
from .model_services.employees_service import EmployeeService

from ..models.models import Company, Contact, Material, Meeting, Employee

from django.utils import timezone

from django.http import JsonResponse

TABLE_MODELS = {
  'companies': Company,
  'contacts': Contact,
  'materials':  Material,
  'meetings': Meeting,
  'employees': Employee
}

TABLE_SERVICES = {
  'companies': CompanyService,
  'contacts': ContactService,
  'materials':  MaterialService,
  'meetings': MeetingService,
  'employees': EmployeeService
}

def model_get(table):
  model = TABLE_MODELS.get(table)
  if model is None:
    raise ValueError(f'Unknown table: {table}')
  return model

def service_get(table):
  service = TABLE_SERVICES.get(table)
  if service is None:
    raise ValueError(f'Unknown table: {table}')
  return service

class CommonService:
  @staticmethod
  def item_update(item, user=None):
    item.update(
      updated_at = timezone.now(),
      updated_by=user
    )

    return True

  def item_create(model, id, user=None):
    model.objects.filter(id=id).update(
      created_at = timezone.now(),
      created_by = user,
      updated_at = timezone.now(),
      updated_by=user
    )

  @staticmethod
  def edit(table, id, input_data, user=None):
    model = model_get(table)
    service = service_get(table)
    item = model.objects.filter(id=id)

    service.edit(item, input_data)
    CommonService.item_update(item, user)

    return True

  @staticmethod
  def add(table, input_data,user=None):
    model = model_get(table)
    service = service_get(table)

    id = service.create(input_data, user)
    CommonService.item_create(model, id, user)

    return id

  @staticmethod
  def delete_item(table, id):
    model = model_get(table)
    item = model.objects.filter(id=id)
    item.delete()

    return True