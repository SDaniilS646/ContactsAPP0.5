from django.db import models

class Meetings(models.Model):
    subject = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    record_link = models.CharField(max_length=255, blank=True, null=True)
    meeting_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)

    contacts = models.ManyToManyField(
        'contacts.Contacts',
        through='apps.MeetingContact',
        related_name='meetings_contact'
    )

    employees = models.ManyToManyField(
        'employees.Employees',
        through='apps.MeetingEmployee',
        related_name='meetings_employee'
    )

    class Meta:
        managed = False
        db_table = 'meetings'