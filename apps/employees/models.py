from django.db import models
from django.contrib.postgres.fields import ArrayField

class Employees(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mail = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employees'