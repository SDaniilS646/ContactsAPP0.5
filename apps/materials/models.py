from django.db import models
from django.contrib.postgres.fields import ArrayField

class Materials(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)  # This field type is a guess.
    updated_at = models.DateTimeField(blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)

    companies = models.ManyToManyField(
        'companies.Companies',
        through='apps.CompanyMaterial',
        related_name='companies_material'
    )


    class Meta:
        managed = False
        db_table = 'materials'