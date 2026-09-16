# from django.db import models

# from .mixins import AuditedModel

# class trainingModel(AuditedModel):
#   name = models.CharField(max_length=10, blank=True)
#   title = models.CharField(max_length=50, blank=True)
#   class Meta:
#       db_table = 'measures'
  
#   def __str__(self):
#       return self.name or f'Ед.Изм #{self.pk}'