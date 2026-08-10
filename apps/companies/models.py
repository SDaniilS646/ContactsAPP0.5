from django.db import models

class Companies(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    inn = models.CharField(max_length=255, blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=255, blank=True, null=True)
    mail = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    contacts = models.ManyToManyField(
        'contacts.Contacts',
        through='apps.CompanyContact',
        related_name='companies_contact'
    )

    materials = models.ManyToManyField(
        'materials.Materials',
        through='apps.CompanyMaterial',
        related_name='companies_contact'
    )

    class Meta:
        managed = False
        db_table = 'companies'
