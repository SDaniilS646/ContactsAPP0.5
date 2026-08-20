from ...models.connections import CompanyContact, CompanyMaterial, MeetingContact, MeetingEmployee, MeetingCompany
from ..common_service import CommonService, TABLE_MODELS, TABLE_SERVICES


CONNECTIONS = {
  ('companies', 'contacts'): {
    'model': CompanyContact, 'field1':'company_id', 'field2':'contact_id', 'extra_fields': ['position', 'mail', 'phone']
  },
  ('companies', 'materials'): {
    'model': CompanyMaterial, 'field1':'company_id', 'field2':'material_id', 'extra_fields': ['is_main']
  },
  ('meetings', 'companies'): {'model': MeetingCompany, 'field1':'meeting_id', 'field2':'company_id'},
  ('meetings', 'contacts'): {'model': MeetingContact, 'field1':'meeting_id', 'field2':'contact_id'},
  ('meetings', 'employees'): {'model': MeetingEmployee, 'field1':'meeting_id', 'field2':'employee_id'},
}

class ConnectionService:
  @staticmethod
  def delete_connection(input_data, user):
    table1 = input_data.get('table1')
    table2 = input_data.get('table2')
    id1 = input_data.get('id1')
    id2 = input_data.get('id2')

    config = CONNECTIONS.get((table1, table2))

    model = config['model']
    model.objects.filter(**{config['field1']: id1, config['field2']: id2}).delete()

    item = TABLE_MODELS.get(table1).objects.filter(id=id1)
    CommonService.item_update(item, user)

    return True

  @staticmethod
  def create_connection(input_data, user):
    table1 = input_data.get('table1')
    table2 = input_data.get('table2')
    id1 = input_data.get('id1')
    id2 = input_data.get('id2')

    config = CONNECTIONS.get((table1, table2))

    model = config['model']
    extras = config.get('extra_fields', [])

    input_extras = input_data.get('extra', {})
    defaults = dict(input_extras)
    print(defaults)

    new_id = model.objects.update_or_create(**{config['field1']: id1, config['field2']: id2}, defaults=defaults)
    
    return
  
  @staticmethod
  def get_company_contact(column, id, id_2=None):
    if column == 'contact':
      return CompanyContact.objects.filter(contact=id)
    elif column == 'company':
      return CompanyContact.objects.filter(company=id)
    elif column == 'company_contact':
      return CompanyContact.objects.filter(company=id, contact=id_2)

  @staticmethod
  def get_companies_contacts(all_company_ids):
    return CompanyContact.objects.filter(company_id__in=all_company_ids)
    
  @staticmethod
  def get_company_material(column, id):
    if column == 'material':
      return CompanyMaterial.objects.filter(material=id)
    elif column == 'company':
      return CompanyMaterial.objects.filter(company=id)
    
  @staticmethod
  def delete_material_connection(comp_id, mat_id):
    id = CompanyMaterial.objects.get(company=comp_id, material=mat_id).id
    CompanyMaterial.objects.filter(id=id).delete()
  
  @staticmethod
  def delete_contact_connection(comp_id, cont_id):
    id = CompanyContact.objects.get(company=comp_id, contact=cont_id).id
    CompanyContact.objects.filter(id=id).delete()
    

  @staticmethod
  def delete_all_contact_connections(comp_id):
    CompanyContact.objects.filter(company=comp_id).delete()

  @staticmethod
  def delete_all_material_connections(comp_id):
    CompanyMaterial.objects.filter(company=comp_id).delete()