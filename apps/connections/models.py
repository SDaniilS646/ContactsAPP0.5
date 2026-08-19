from django.db import models
from apps.companies.models import Company
from apps.contacts.models import Contact
from apps.materials.models import Material
from apps.meetings.models import Meeting
from apps.employees.models import Employee

from django.conf import settings

class CompanyContact(models.Model):
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
    position = models.CharField(max_length=255, blank=True)
    mail = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name='+', on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name='+', on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = ('company', 'contact')
        db_table = 'company_contact'

class CompanyMaterial(models.Model):
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

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, null=True, blank=True,
            related_name='+', on_delete=models.SET_NULL
        )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name='+', on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = ('company', 'material')
        db_table = 'company_material'

class MeetingContact(models.Model):
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE,
        related_name='meeting_contacts'
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE,
        related_name='meeting_contacts'
    )

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, null=True, blank=True,
            related_name='+', on_delete=models.SET_NULL
        )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name='+', on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = ('meeting', 'contact')
        db_table = 'meeting_contact'

class MeetingEmployee(models.Model):
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE,
        related_name='meeting_employees'
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='meeting_employees'
    )
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, null=True, blank=True,
            related_name='+', on_delete=models.SET_NULL
        )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name='+', on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = ('meeting', 'employee')
        db_table = 'meeting_employee'

class MeetingCompany(models.Model):
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, 
        related_name='meeting_companies'
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, 
        related_name='meeting_companies'
    )
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, null=True, blank=True,
            related_name='+', on_delete=models.SET_NULL
        )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name='+', on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = ('meeting', 'company')
        db_table = 'meeting_company'