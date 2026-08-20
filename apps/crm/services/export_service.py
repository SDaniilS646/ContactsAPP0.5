from apps.crm.services.model_services.company_service import CompanyService
from apps.crm.services.model_services.connection_service import ConnectionService

class ExportService:
  @staticmethod
  def get_companies_output(companies_ids):
    output_companies = CompanyService.companies_filter_ids(companies_ids).prefetch_related('contacts', 'materials')
    output_data = []

    all_connections = ConnectionService.get_companies_contacts(companies_ids)
    connections_by_company = {}

    for conn in all_connections:
      connections_by_company.setdefault(conn.company_id, []).append(conn)
  
    for company in output_companies:
      comp_cont = connections_by_company.get(company.id, [])
        
      contacts = company.contacts.all()
    
      materials = company.materials.all()
      materials_list = '; '.join([material.name for material in materials])
      company_contacts = {
        'name': [],
        'mail': [],
        'phone': []
      }
      if company.mail:
        company_contacts['mail'].append(company.mail)
      if company.phone:
        company_contacts['phone'].append(company.phone)

      for cont in contacts:
        connection = next((item for item in comp_cont if item.contact_id == cont.id), None)
        company_contacts['name'].append(f'{cont.last_name} {cont.first_name}')

        if connection and connection.mail: 
          company_contacts['mail'].append(connection.mail)
        if connection and connection.phone:
          company_contacts['phone'].append(connection.phone)

      output_data.append({
        'company_name': company.name,
        'names': '; '.join(company_contacts['name']),
        'mails': '; '.join(company_contacts['mail']),
        'phones': '; '.join(company_contacts['phone']),
        'materials': materials_list
      })

    return output_data