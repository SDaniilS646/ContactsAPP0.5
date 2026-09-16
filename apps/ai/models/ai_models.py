from django.db import models

from .mixins import AuditedModel

class senderAiLog(AuditedModel):
  user_query = models.TextField()
  system_query = models.TextField()
  db_context = models.JSONField()
  model_response = models.TextField()
  user_rating = models.CharField(max_length=16, default='pending')
  correct_response = models.TextField(blank=True)

  class Meta:
      db_table = 'sender_ai_log'
