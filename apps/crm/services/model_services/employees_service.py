from ...models.models import Employee
from django.utils import timezone

class EmployeeService:
  @staticmethod
  def get_employees():
    return Employee.objects.all()
  
  @staticmethod
  def get_employee(emp_id):
    return Employee.objects.get(id=emp_id)
  
  @staticmethod
  def item_update(emp_id):
    Employee.objects.filter(id=emp_id).update(updated_at = timezone.now())
    return
  
  @staticmethod
  def create(input_data, user):
    new_id = Employee.objects.create(
      first_name = input_data['first_name'],
      last_name = input_data['last_name'],
      patronymic = input_data['patronymic'],
      phone = input_data['phone'],
      mail = input_data['mail']
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
      updated_at = timezone.now()
    )

    return
  