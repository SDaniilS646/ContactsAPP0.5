from apps.companies.models import Companies
from django.utils import timezone

class CompanyService:
  @staticmethod
  def get_companies():
    return Companies.objects.all()
  
  @staticmethod
  def get_company(comp_id):
    return Companies.objects.get(id=comp_id)
  
  @staticmethod
  def item_update(comp_id):
    Companies.objects.filter(id=comp_id).update(updated_at = timezone.now())
    return

  @staticmethod
  def set_company(input_data):
    new_id = Companies.objects.create(
      name = input_data['company_name'],
      inn = input_data['inn'],
      site = input_data['site'],
      rating = input_data['rating'],
      mail = input_data['mail'],
      phone = input_data['phone'],
      comment = input_data['comment'],
      added_at = timezone.now(),
      updated_at = timezone.now()
    ).id

    return new_id
  
  @staticmethod
  def edit_company(input_data):
    comp_id = input_data['id']
    Companies.objects.filter(id=comp_id).update(
      name = input_data['company_name'],
      inn = input_data['inn'],
      site = input_data['site'],
      rating = input_data['rating'],
      mail = input_data['mail'],
      phone = input_data['phone'],
      comment = input_data['comment'],
      updated_at = timezone.now()
    )

  @staticmethod
  def delete(id):
    Companies.objects.filter(id=id).delete()
    return