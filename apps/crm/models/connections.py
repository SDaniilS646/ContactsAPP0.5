from django.db import models
from django.conf import settings

from .models import Company, Contact, Material, Meeting, Employee, Object
from .mixins import AuditedModel, PersonNameModel, ContactsModel


class CompanyContact(AuditedModel, ContactsModel):
  company = models.ForeignKey(
      Company, 
      on_delete=models.CASCADE,
      related_name='company_contacts'
  )
  contact = models.ForeignKey(
      Contact,
      on_delete=models.CASCADE,
      related_name='company_contacts'
  )
  position = models.CharField(max_length=255, blank=True, null=True)

  class Meta:
      unique_together = ('company', 'contact')
      db_table = 'company_contact'

class CompanyMaterial(AuditedModel):
  company = models.ForeignKey(
      Company,
      on_delete=models.CASCADE,
      related_name='company_materials'
  )
  material = models.ForeignKey(
      Material,
      on_delete=models.CASCADE,
      related_name='company_materials'
  )
  is_main = models.BooleanField(default=False)

  class Meta:
      unique_together = ('company', 'material')
      db_table = 'company_material'

class MeetingContact(AuditedModel):
  meeting = models.ForeignKey(
      Meeting, on_delete=models.CASCADE,
      related_name='meeting_contacts'
  )
  contact = models.ForeignKey(
      Contact, on_delete=models.CASCADE,
      related_name='meeting_contacts'
  )

  class Meta:
      unique_together = ('meeting', 'contact')
      db_table = 'meeting_contact'

class MeetingEmployee(AuditedModel):
  meeting = models.ForeignKey(
      Meeting, on_delete=models.CASCADE,
      related_name='meeting_employees'
  )
  employee = models.ForeignKey(
      Employee, on_delete=models.CASCADE,
      related_name='meeting_employees'
  )

  class Meta:
      unique_together = ('meeting', 'employee')
      db_table = 'meeting_employee'

class MeetingCompany(AuditedModel):
  meeting = models.ForeignKey(
      Meeting, on_delete=models.CASCADE, 
      related_name='meeting_companies'
  )
  company = models.ForeignKey(
      Company, on_delete=models.CASCADE, 
      related_name='meeting_companies'
  )

  class Meta:
      unique_together = ('meeting', 'company')
      db_table = 'meeting_company'

class BrendList(AuditedModel):
    object = models.ForeignKey(
      Object, on_delete=models.CASCADE, 
      related_name='brend_list'
    )
    company = models.ForeignKey(
      Company, on_delete=models.CASCADE, 
      related_name='brend_list'
    )
    material = models.ForeignKey(
      Material, on_delete=models.CASCADE, 
      related_name='brend_list'
    )
    section = models.CharField(max_length=255, blank=True, verbose_name='раздел')

    class Meta:
        unique_together = ('object', 'company')
        db_table = 'brend_list'