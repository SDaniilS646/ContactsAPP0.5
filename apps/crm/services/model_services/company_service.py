from ...models.models import Company
from django.utils import timezone
from django.db import transaction



class CompanyService:
  @staticmethod
  def get_companies():
    return Company.objects.all()
  
  @staticmethod
  def get_company(comp_id):
    return Company.objects.get(id=comp_id)

  @staticmethod
  def create(input_data, user):
    company_contacts = input_data.get('company_contacts', [])
    company_materials = input_data.get('company_materials', [])
    new_id = None
    with transaction.atomic():
      new_id = Company.objects.create(
        name = input_data['company_name'],
        inn = None if input_data['inn']=='' else input_data['inn'],
        site = input_data['site'],
        rating = input_data['rating'],
        mail = input_data['mail'],
        phone = input_data['phone'],
        comment = input_data['comment']
      ).id

      if len(company_contacts) > 0 or len(company_materials) > 0:
        from .connection_service import ConnectionService

      if len(company_contacts) > 0:
        for contact in company_contacts:
          connection_input = {
            'table1': 'companies',
            'table2': 'contacts',
            'id1': new_id,
            'id2': contact['id'],
            'extra': {
              'position': contact['position'], 
              'mail': contact['corp-mail'], 
              'phone': contact['corp-phone']
            }
          }
          ConnectionService.create_connection(connection_input, user)
      if len(company_materials) > 0:
        for material in company_materials:
          connection_input = {
            'table1': 'companies',
            'table2': 'materials',
            'id1': new_id,
            'id2': material['id'],
            'extra': {
              'is_main': material['is_main']
            }
          }
          ConnectionService.create_connection(connection_input, user)
    return new_id
  
  @staticmethod
  def edit(item, input_data):
    item.update(
      name = input_data['company_name'],
      inn = None if input_data['inn']=='' else input_data['inn'],
      site = input_data['site'],
      rating = input_data['rating'],
      mail = input_data['mail'],
      phone = input_data['phone'],
      comment = input_data['comment']
    )

  @staticmethod
  def companies_filter_ids(companies_ids):
    return Company.objects.filter(id__in=companies_ids)