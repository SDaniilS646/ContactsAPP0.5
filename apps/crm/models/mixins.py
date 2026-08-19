from django.db import models
from django.conf import settings

class AuditedModel(models.Model):
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
    abstract = True

class PersonNameModel(models.Model):
  first_name = models.CharField(max_length=255, blank=True, null=True)
  last_name = models.CharField(max_length=255, blank=True, null=True)
  patronymic = models.CharField(max_length=255, blank=True, null=True)
  
  class Meta:
    abstract = True

class ContactsModel(models.Model):
  phone = models.CharField(max_length=50, blank=True, null=True)
  mail = models.CharField(max_length=255, blank=True, null=True)

  class Meta:
    abstract = True
