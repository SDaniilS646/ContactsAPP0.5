from django.db import models


class Contacts(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    is_main = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    companies = models.ManyToManyField(
        'companies.Companies',
        through='apps.CompaniesContacts',
        related_name='contact_companies'
    )

    class Meta:
        managed = False
        db_table = 'contacts'
        db_table_comment = 'Контактные лица'