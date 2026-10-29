from django.db import models
from django.conf import settings


from .mixins import AuditedModel, PersonNameModel, ContactsModel

class Contact(AuditedModel, PersonNameModel, ContactsModel):
  comment = models.TextField(blank=True)

  class Meta:
      db_table = 'contacts'

  def __str__(self):
      return self.last_name or f'Контакт #{self.pk}'

class Employee(AuditedModel, PersonNameModel, ContactsModel):
  position = models.CharField(max_length=255, blank=True)

  class Meta:
      db_table = 'employees'

  def __str__(self):
      return self.last_name or f'Сотрудник #{self.pk}'

class Measure(AuditedModel):
  name = models.CharField(max_length=10, blank=True)
  title = models.CharField(max_length=50, blank=True)
  class Meta:
      db_table = 'measures'
  
  def __str__(self):
      return self.name or f'Ед.Изм #{self.pk}'

class Material(AuditedModel):
  name = models.CharField(max_length=255, blank=True, verbose_name='Название')
  parent = models.ForeignKey(
      'self', null=True, blank=True,
      related_name='children', verbose_name='Родительский материал', on_delete=models.PROTECT
  ) # Возможна замена на category FK + новая модель category (пока под вопросом)
  measure = models.ForeignKey(Measure, blank=True, null=True, on_delete=models.SET_NULL)
  keywords = models.TextField(blank=True)

  class Meta:
      db_table = 'materials'

  def __str__(self):
      return self.name or f'Материал #{self.pk}'

class Object(AuditedModel):
    name = models.CharField(max_length=255, blank=True, verbose_name='Название')

    class Meta:
        db_table = 'objects'
    def __str__(self):
        return self.name or f'Объект #{self.pk}'

class Company(AuditedModel, ContactsModel):
  name = models.CharField(max_length=255, blank=True)
  inn = models.CharField(max_length=20, blank=True, null=True, unique=True)
  site = models.CharField(max_length=255, blank=True)
  rating = models.IntegerField(blank=True, null=True)

  comment = models.TextField(blank=True)

  contacts = models.ManyToManyField(
      Contact,
      through='CompanyContact',
      related_name='companies'
  )

  materials = models.ManyToManyField(
      Material,
      through='CompanyMaterial',
      related_name='companies'
  )

  class Meta:
      db_table = 'companies'
      verbose_name = 'Компания'
      verbose_name_plural = 'Компании'

  def __str__(self):
      return self.name or f'Компания #{self.pk}'

class Meeting(AuditedModel):
    subject = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    record_link = models.CharField(max_length=255, blank=True)

    meeting_date = models.DateTimeField(blank=True, null=True)


    contacts = models.ManyToManyField(
        Contact,
        through='MeetingContact',
        related_name='meetings'
    )

    employees = models.ManyToManyField(
        Employee,
        through='MeetingEmployee',
        related_name='meetings'
    )

    companies = models.ManyToManyField(
        Company,
        through='MeetingCompany',
        related_name='meetings'
    )

    class Meta:
        db_table = 'meetings'

    def __str__(self):
        return self.subject or f'Встреча #{self.pk}'

class ExportLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name='+', on_delete=models.SET_NULL
    )
    file_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'export_log'

# class Brend(AuditedModel):
#     name = models.CharField(max_length=255, blank=True)
#     rating = models.IntegerField(blank=True, null=True)
#     site = models.CharField(max_length=255, blank=True)
#     comment = models.TextField(blank=True)

#     country = models.CharField(max_length=50, blank=True)

#     materials = models.ManyToManyField(
#         Material,
#         through='BrendsMaterial',
#         related_name='brends'
#     )

#     class Meta:
#         db_table = 'brends'
#         verbose_name = 'Бренд'
#         verbose_name_plural = 'Бренды'

#     def __str__(self):
#         return self.name or f'Бренд #{self.pk}'