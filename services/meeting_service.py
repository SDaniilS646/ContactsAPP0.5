from apps.meetings.models import Meetings
from django.utils import timezone

class MeetingService:
  @staticmethod
  def get_meetings():
    return Meetings.objects.all()
  
  @staticmethod
  def set_meeting(input_data):
    new_id = Meetings.objects.create(
      subject = input_data['subject'],
      comment = input_data['comment'],
      record_link = input_data['record_link'],
      meeting_date = input_data['meeting_date'],
      updated_at = timezone.now(),
      added_at = timezone.now()
    ).id
    return new_id

  @staticmethod
  def get_meeting(id):
    return Meetings.objects.get(id=id)
  
  @staticmethod
  def delete(id):
    Meetings.objects.filter(id=id).delete()
    return
