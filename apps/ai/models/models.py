from django.db import models

from .mixins import AuditedModel
from apps.crm.models.models import Material

class AiTask(AuditedModel):
  name = models.CharField(max_length=255, unique=True)
  description = models.TextField(blank=True)

  class Meta:
    db_table = 'ai_task'

class AiTaskVersion(AuditedModel):
  task = models.ForeignKey(AiTask, on_delete=models.CASCADE, related_name='versions')
  version = models.PositiveIntegerField()

  system_prompt = models.TextField()
  model_name = models.CharField(max_length=255)
  lora_adapter_path = models.CharField(max_length=512, blank=True)
  temperature = models.FloatField(default=0.0)
  max_tokens = models.PositiveIntegerField(default=2048)
  response_format = models.JSONField(null=True, blank=True)

  is_active = models.BooleanField(default=False)
  notes = models.TextField(blank=True)

  class Meta:
    unique_together = [('task', 'version')]
    ordering = ['-version']
    db_table = 'ai_task_version'

class AiQueryLog(AuditedModel):
  # task = models.ForeignKey(AiTask, on_delete=models.CASCADE, related_name='logs')
  task_version = models.ForeignKey(AiTaskVersion, null=True, on_delete=models.SET_NULL, related_name='logs')

  request_text = models.TextField()
  # input_payload = models.JSONField()

  raw_response = models.TextField()
  # parsed_response = models.JSONField(null=True)
  # resolution = models.CharField(max_length=32)
  latency_ms = models.PositiveIntegerField(null=True)
  token_count = models.PositiveIntegerField(null=True)
  prompt_tokens = models.PositiveIntegerField(null=True)

  # rating = models.CharField(max_length=25)
  # comment = models.TextField(blank=True)
  # corrected_response = models.JSONField(null=True, blank=True)

  class Meta:
    db_table = 'ai_query_log'

  
class AiExample(AuditedModel):
  request = models.ForeignKey(AiQueryLog, on_delete=models.SET_NULL, related_name='example_log', null=True) # Какая модель
  source = models.CharField(max_length=32, default='manual') # Для истории - ИИ сделал, юзер прочекал или юзер сделал

  # request | material  | check
  # ----------------------------
  # Бетон   | Бетон(FK) | True
  # Бетон   | Гранит(FK)| False
  request_text = models.TextField() # user_request
  materials = models.ForeignKey(
      Material, on_delete=models.CASCADE, 
      related_name='output_example'
    ) # FK на Materials
  
  example_check = models.BooleanField(null=True, blank=True) # Bool

  # embedding = models.BinaryField(null=True, blank=True) # вектор для ML

  is_active = models.BooleanField(default=True)

  class Meta:
    db_table = 'ai_example'