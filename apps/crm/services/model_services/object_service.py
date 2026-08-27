from ...models.models import Object

class ObjectService:
  @staticmethod
  def get_objects():
    return Object.objects.all()

  @staticmethod
  def create(input_data, user):
    new_id = Object.objects.create(
      name = input_data['name']
    ).id
    return new_id