from apps.contacts.models import Contacts
from django.utils import timezone

class ContactService:
  @staticmethod
  def get_contacts():
    return Contacts.objects.all()
  
  @staticmethod
  def get_contact(cont_id):
    return Contacts.objects.get(id=cont_id)
  
  @staticmethod
  def item_update(cont_id):
    Contacts.objects.filter(id=cont_id).update(updated_at = timezone.now())
    return
  
  @staticmethod
  def set_contact(input_data):
    new_id = Contacts.objects.create(
      first_name = input_data['first_name'],
      last_name = input_data['last_name'],
      patronymic = input_data['patronymic'],
      phone = input_data['phone'],
      mail = input_data['mail'],
      comment = input_data['comment'],
      added_at = timezone.now(),
      updated_at = timezone.now()
    ).id

    return new_id
  
  @staticmethod
  def edit_contact(input_data):
    cont_id = input_data['id']
    Contacts.objects.filter(id=cont_id).update(
      first_name = input_data['first_name'],
      last_name = input_data['last_name'],
      patronymic = input_data['patronymic'],
      phone = input_data['phone'],
      mail = input_data['mail'],
      comment = input_data['comment'],
      updated_at = timezone.now()
    )

    return
  
  @staticmethod
  def delete(id):
    Contacts.objects.filter(id=id).delete()
    return