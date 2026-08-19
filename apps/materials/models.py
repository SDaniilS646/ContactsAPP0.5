from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

class Material(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name='Название')
    parent_id = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children', verbose_name='Родительский материал', on_delete=models.PROTECT
    ) # Возможна замена на category FK + новая модель category (пока под вопросом)
    measure = models.ForeignKey('Measure', blank=True, null=True, ondelete=models.SET_NULL)

    keywords = models.TextField(blank=True)  # This field type is a guess.

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
        db_table = 'materials'

    def __str__(self):
        return self.name or f'Материал #{self.pk}'

class Measure(models.Model):
    name = models.CharField(max_length=10, blank=True)
    class Meta:
        db_table = 'measures'
    
    def __str__(self):
        return self.name or f'Ед.Изм #{self.pk}'