from django.db import models
from apps.companies.models import Companies
from apps.contacts.models import Contacts
from apps.materials.models import Materials


class CompaniesContacts(models.Model):
  company = models.ForeignKey(
    Companies,
    on_delete=models.DO_NOTHING
  )

  contact = models.ForeignKey(
    Contacts,
    on_delete=models.DO_NOTHING,
  )
  role_in_company = models.CharField(max_length=100, blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    db_table = 'company_contacts'

class CompaniesMaterials(models.Model):
  company = models.ForeignKey(
    Companies,
    on_delete=models.DO_NOTHING
  )

  materials = models.ForeignKey(
    Materials,
    on_delete=models.DO_NOTHING,
    db_column='material_id'
  )
  
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    db_table = 'company_materials'