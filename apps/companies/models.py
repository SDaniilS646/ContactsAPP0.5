from django.db import models
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=255, blank=True)
    inn = models.CharField(max_length=20, blank=True, null=True, unique=True)
    site = models.CharField(max_length=255, blank=True)
    rating = models.IntegerField(blank=True, null=True)
    mail = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
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

    contacts = models.ManyToManyField(
        'contacts.Contact',
        through='connections.CompanyContact',
        related_name='companies'
    )

    materials = models.ManyToManyField(
        'materials.Material',
        through='connections.CompanyMaterial',
        related_name='companies'
    )

    class Meta:
        db_table = 'companies'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['-created_at']

    def __str__(self):
        return self.name or f'Компания #{self.pk}'
