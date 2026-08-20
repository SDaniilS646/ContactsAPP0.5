from ...models.models import Meeting
from django.utils import timezone
from django.db import transaction

class MeetingService:
  @staticmethod
  def get_meetings():
    return Meeting.objects.all()
  
  @staticmethod
  def create(input_data, user):
    meeting_company = input_data.get('meeting_companies', [])
    meeting_contact = input_data.get('meeting_contacts', [])
    meeting_employee = input_data.get('meeting_employees', [])
    new_id = None
    with transaction.atomic():
      new_id = Meeting.objects.create(
        subject = input_data['subject'],
        comment = input_data['comment'],
        record_link = input_data['record_link'],
        meeting_date = input_data['meeting_date']
      ).id

      if len(meeting_company) > 0 or len(meeting_contact) > 0 or len(meeting_employee) > 0:
        from .connection_service import ConnectionService

      if len(meeting_company) > 0:
        for company in meeting_company:
          connection_input = {
            'table1': 'meetings',
            'table2': 'companies',
            'id1': new_id,
            'id2': company['id'],
          }
          ConnectionService.create_connection(connection_input, user)
      if len(meeting_contact) > 0:
        for contact in meeting_contact:
          connection_input = {
            'table1': 'meetings',
            'table2': 'contacts',
            'id1': new_id,
            'id2': contact['id'],
          }
          ConnectionService.create_connection(connection_input, user)
      if len(meeting_employee) > 0:
        for employee in meeting_employee:
          connection_input = {
            'table1': 'meetings',
            'table2': 'employees',
            'id1': new_id,
            'id2': employee['id'],
          }
          ConnectionService.create_connection(connection_input, user)


    return new_id

  @staticmethod
  def get_meeting(id):
    return Meeting.objects.get(id=id)
  
