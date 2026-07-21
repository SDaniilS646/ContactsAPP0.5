from django.db import models
from apps.companies.models import Companies
from apps.contacts.models import Contacts
from apps.materials.models import Materials
from apps.meetings.models import Meetings
from apps.employees.models import Employees

class CompanyContact(models.Model):
    company = models.ForeignKey(
        Companies, 
        on_delete=models.CASCADE
    )
    contact = models.ForeignKey(
        Contacts,
        on_delete=models.CASCADE
    )
    position = models.CharField(max_length=255, blank=True, null=True)
    mail = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_contact'


class CompanyMaterial(models.Model):
    company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        Materials,
        on_delete=models.CASCADE
    )
    is_main = models.BooleanField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_material'


class MeetingContact(models.Model):
    meeting = models.ForeignKey(Meetings, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meeting_contact'


class MeetingEmployee(models.Model):
    meeting = models.ForeignKey(Meetings, on_delete=models.CASCADE)
    emloyee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meeting_employee'