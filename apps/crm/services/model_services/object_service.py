from ...models.models import Object

class ObjectService:
  @staticmethod
  def get_objects():
    return Object.objects.all()

  @staticmethod
  def get_object(id):
    return Object.objects.filter(id=id).first()

  @staticmethod
  def create(input_data, user):
    new_id = Object.objects.create(
      name = input_data['name']
    ).id
    return new_id

  @staticmethod
  def edit(item, input_data):
    print(item)
    item.update(
      name = input_data['name']
    )
    return