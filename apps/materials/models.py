from django.db import models
from django.contrib.postgres.fields import ArrayField

class Materials(models.Model):
    name = models.CharField(unique=True, max_length=255)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, db_comment='Родительская категория (для иерархии)')
    keywords = ArrayField(models.CharField(max_length=255), default=list, blank=True, null=True, db_comment='Дополнительные ключевые слова для поиска')  # This field type is a guess.
    is_active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


    companies = models.ManyToManyField(
        'companies.Companies',
        through='apps.CompaniesMaterials',
        related_name='material_companies'
    )

    class Meta:
        managed = False
        db_table = 'materials'
        db_table_comment = 'Справочник материалов и категорий'