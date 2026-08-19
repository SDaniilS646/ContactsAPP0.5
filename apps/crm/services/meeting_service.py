from ..models.models import Meeting
from django.utils import timezone

class MeetingService:
  @staticmethod
  def get_meetings():
    return Meeting.objects.all()
  
  @staticmethod
  def set_meeting(input_data):
    new_id = Meeting.objects.create(
      subject = input_data['subject'],
      comment = input_data['comment'],
      record_link = input_data['record_link'],
      meeting_date = input_data['meeting_date'],
      updated_at = timezone.now(),
      created_at = timezone.now()
    ).id
    return new_id

  @staticmethod
  def get_meeting(id):
    return Meeting.objects.get(id=id)
  
  @staticmethod
  def delete(id):
    Meeting.objects.filter(id=id).delete()
    return
