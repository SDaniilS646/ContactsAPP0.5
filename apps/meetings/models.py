from django.db import models
from django.conf import settings

class Meeting(models.Model):
    subject = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    record_link = models.CharField(max_length=255, blank=True)
    
    meeting_date = models.DateTimeField(blank=True, null=True)

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
        through='connections.MeetingContact',
        related_name='meetings'
    )

    employees = models.ManyToManyField(
        'employees.Employee',
        through='connections.MeetingEmployee',
        related_name='meetings'
    )

    companies = models.ManyToManyField(
        'companies.Company',
        through='connections.MeetingCompany',
        related_name='meetings'
    )

    class Meta:
        db_table = 'meetings'

    def __str__(self):
        return self.subject or f'Встреча #{self.pk}'