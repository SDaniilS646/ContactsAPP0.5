from apps.connections.models import CompanyContact, CompanyMaterial, MeetingContact, MeetingEmployee, MeetingCompany
from apps.crm.services.company_service import CompanyService
from apps.crm.services.material_service import MaterialService
from apps.crm.services.contact_service import ContactService
from apps.crm.services.meeting_service import MeetingService
from apps.crm.services.employees_service import EmployeeService

from ..models.models import Company

from django.utils import timezone

TABLE_MODELS = {
  'companies': Company
}

class CommonService:
  @staticmethod
  def item_update(table, id, user=None):
    model = TABLE_MODELS.get(table)
    if model is None:
      raise ValueError(f'Unknown table: {table}')

    upd = model.objects.filter(id=id).update(
      updated_at = timezone.now(),
      updated_by=user
    )
    print(upd)

    return True