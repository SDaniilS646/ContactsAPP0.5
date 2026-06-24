from django.db import models

class Companies(models.Model):
    name = models.CharField(max_length=255, db_comment='Название компании')
    inn = models.CharField(unique=True, max_length=12, blank=True, null=True, db_comment='ИНН (уникальный)')
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    rating = models.SmallIntegerField(blank=True, null=True, db_comment='Рейтинг от 0 до 5')
    is_active = models.BooleanField(blank=True, null=True, db_comment='Активна ли компания')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    contacts = models.ManyToManyField(
        'contacts.Contacts',
        through='apps.CompaniesContacts',
        related_name='company_contacts'
    )

    materials = models.ManyToManyField(
        'materials.Materials',
        through='apps.CompaniesMaterials',
        related_name='company_materials'
    )

    class Meta:
        managed = False
        db_table = 'companies'
        db_table_comment = 'Компании-поставщики и производители'