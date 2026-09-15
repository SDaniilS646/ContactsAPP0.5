from django.db import models
from django.conf import settings


class TempVorData(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='temp_data_created', on_delete=models.SET_NULL)
  section = models.TextField()
  work = models.TextField()
  material = models.TextField()
  measure = models.TextField()
  amount = models.TextField()
  type = models.TextField()
  category  = models.TextField()
  filename = models.TextField()
  filedir = models.TextField()
  file_row = models.IntegerField()

  created_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    db_table = 'temp_vor'



class TrainingExample(models.Model):
  STATUS_CHOICES = [
    ('pending', 'Ожидает разметки'),
    ('labeled', 'Размечено'),
    ('reviewed', 'Проверено')
  ]

  text = models.TextField()
  # input_data = models.JSONField()
  label = models.CharField(max_length=100, null=True, blank=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

  uncertainity_score = models.FloatField(null=True, blank=True)
  predicted_label = models.CharField(max_length=100, null=True, blank=True)

  created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='training_created', on_delete=models.SET_NULL)
  labeled_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='training_labeled', on_delete=models.SET_NULL)
  created_at = models.DateTimeField(blank=True, null=True)
  labeled_at = models.DateTimeField(blank=True, null=True)

  used_in_model_version = models.ForeignKey(
    'ModelVersion', null=True, related_name='training_examples', on_delete=models.SET_NULL
  )

  class Meta:
    db_table = 'training_example'

  def __str__(self):
    return f'Example #{self.id} — {self.status} ({self.label or 'без метки'})'

class ModelVersion(models.Model):
  version = models.PositiveIntegerField()
  model_type = models.CharField(max_length=100)

  trained_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
  trained_at = models.DateTimeField(blank=True, null=True)

  Training_examples_count  = models.PositiveIntegerField()
  metrics = models.JSONField(default=dict)

  is_active = models.BooleanField(default=False)

  class Meta:
    db_table = 'model_version'

  def __str__(self):
    active_marker = ' [АКТИВНА]' if self.is_active else ''
    return f'Модель v{self.version}{active_marker}'

class ModelFile(models.Model):
  model_version = models.ForeignKey(ModelVersion, related_name='files', on_delete=models.CASCADE)
  file = models.CharField(max_length=50)
  file_path = models.CharField(max_length=500)

  created_at = models.DateTimeField(blank=True, null=True)
  created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name='+', on_delete=models.SET_NULL
    )

  class Meta:
    db_table = 'model_file'