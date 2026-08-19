from ..models.models import Company
from django.utils import timezone

class CompanyService:
  @staticmethod
  def get_companies():
    return Company.objects.all()
  
  @staticmethod
  def get_company(comp_id):
    return Company.objects.get(id=comp_id)
  
  @staticmethod
  def item_update(comp_id, user_name=None):
    Company.objects.filter(id=comp_id).update(
      updated_at = timezone.now(),
      updated_by=user_name
    )
    return

  @staticmethod
  def set_company(input_data):
    new_id = Company.objects.create(
      name = input_data['company_name'],
      inn = None if input_data['inn']=='' else input_data['inn'],
      site = input_data['site'],
      rating = input_data['rating'],
      mail = input_data['mail'],
      phone = input_data['phone'],
      comment = input_data['comment'],
      created_at = timezone.now(),
      updated_at = timezone.now(),
      # created_by = input_data['user'],
      # updated_by = input_data['user']
    ).id

    return new_id
  
  @staticmethod
  def edit_company(input_data):
    comp_id = input_data['id']
    Company.objects.filter(id=comp_id).update(
      name = input_data['company_name'],
      inn = input_data['inn'],
      site = input_data['site'],
      rating = input_data['rating'],
      mail = input_data['mail'],
      phone = input_data['phone'],
      comment = input_data['comment'],
      updated_at = timezone.now(),
      updated_by = input_data['user']
    )

  @staticmethod
  def delete(id):
    Company.objects.filter(id=id).delete()
    return

  @staticmethod
  def companies_filter_ids(companies_ids):
    return Company.objects.filter(id__in=companies_ids)