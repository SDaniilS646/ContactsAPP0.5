from django.db import models
from django.conf import settings


class Contact(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    patronymic = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    mail = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)

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
        db_table = 'contacts'

    def __str__(self):
        return self.last_name or f'Контакт #{self.pk}'