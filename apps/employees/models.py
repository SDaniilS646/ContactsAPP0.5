from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

class Employee(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    patronymic = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    mail = models.CharField(max_length=255, blank=True)

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
        db_table = 'employees'

    def __str__(self):
        return self.last_name or f'Сотрудник #{self.pk}'