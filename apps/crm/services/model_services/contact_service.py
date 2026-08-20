from ...models.models import Contact
from django.utils import timezone

class ContactService:
  @staticmethod
  def get_contacts():
    return Contact.objects.all()
  
  @staticmethod
  def get_contact(cont_id):
    return Contact.objects.get(id=cont_id)
  
  @staticmethod
  def item_update(cont_id):
    Contact.objects.filter(id=cont_id).update(updated_at = timezone.now())
    return
  
  @staticmethod
  def create(input_data, user):
    new_id = Contact.objects.create(
      first_name = input_data['first_name'],
      last_name = input_data['last_name'],
      patronymic = input_data['patronymic'],
      phone = input_data['phone'],
      mail = input_data['mail'],
      comment = input_data['comment']
    ).id

    return new_id
  
  @staticmethod
  def edit(item, input_data):
    item.update(
      first_name = input_data['first_name'],
      last_name = input_data['last_name'],
      patronymic = input_data['patronymic'],
      phone = input_data['phone'],
      mail = input_data['mail'],
      comment = input_data['comment']
    )

    return