from django.shortcuts import render
from django.http import JsonResponse


from services.company_service import CompanyService
from services.material_service import MaterialService
from services.contact_service import ContactService
from services.connection_service import ConnectionService

from services.contact_service import ContactService

import json


from django.contrib.auth.decorators import login_required

from backend.web_parser.config import SEARCH_PROVIDER, LOADER, EXTRACTOR

from urllib.parse import urlparse

def company_create(request):
  input_data = json.loads(request.body)

  old_companies = CompanyService.get_companies()
  comp_name = input_data['company_name']
  comp_mail = input_data['mail']

  old_companies_names = [item.name for item in old_companies]
  old_companies_mails = [item.mail for item in old_companies]

  if comp_name in old_companies_names or (comp_mail and comp_mail in old_companies_mails):
    print('exists')
    return JsonResponse({
      'Success': False,
      'result': 'Exists'
    })
  
  new_comp_id = CompanyService.set_company(input_data)

  company_contacts = input_data['company_contacts']
  company_materials = input_data['company_materials']

  if company_contacts:
    for contact in company_contacts:
      ConnectionService.set_company_contact(
        {
          'comp_id': new_comp_id,
          'cont_id': contact['id'],
          'cont_mail': contact['corp-mail'],
          'cont_phone': contact['corp-phone'],
          'cont_position': contact['position']
        }
      )
  if company_materials:
    mat_list = []
    for mat in company_materials:
      temp = []
      temp = MaterialService.getAllParents(mat)
      mat_list.extend(temp)
    company_materials = list(set(mat_list))
    for material in company_materials:
      ConnectionService.set_company_material(
        {
          'comp_id': new_comp_id,
          'mat_id': material
        }
      )

  return JsonResponse({
    'success': True,
    'comp_name': comp_name,
    'comp_id':new_comp_id
  })

def delete_connection(request):
  input_data = json.loads(request.body)

  if input_data['table'] == 'comp_mat':
    ConnectionService.delete_material_connection(input_data['id_1'], input_data['id_2'])
  elif input_data['table'] == 'comp_cont':
    ConnectionService.delete_contact_connection(input_data['id_1'], input_data['id_2'])
    ContactService.item_update(input_data['id_2'])

  CompanyService.item_update(input_data['id_1'])

  return JsonResponse({
    'success': True
  })

def edit_contact_list(request):
  input_data = json.loads(request.body)

  company_contacts = input_data['company_contacts']

  ConnectionService.delete_all_contact_connections(input_data['id'])

  if company_contacts:
    for contact in company_contacts:
      ConnectionService.edit_company_contact(
        {
          'comp_id': input_data['id'],
          'cont_id': contact['id'],
          'cont_mail': contact['corp-mail'],
          'cont_phone': contact['corp-phone'],
          'cont_position': contact['position']
        }
      )
      ContactService.item_update(contact['id'])

  CompanyService.item_update(input_data['id'])
  

  return JsonResponse({
    'success': True
  })

def edit_material_list(request):
  input_data = json.loads(request.body)

  company_materials = input_data['company_materials']

  ConnectionService.delete_all_material_connections(input_data['id'])

  if company_materials:
    for material in company_materials:
      ConnectionService.edit_company_material(
        {
          'comp_id': input_data['id'],
          'mat_id': material
        }
      )

  CompanyService.item_update(input_data['id'])

  return JsonResponse({
    'success': True
  })

def delete(request):
  input_data = json.loads(request.body)

  CompanyService.delete(input_data['id'])

  return JsonResponse({
    'success': True
  })

def company_edit(request):
  input_data = json.loads(request.body)

  CompanyService.edit_company(input_data)

  return JsonResponse({
    'success': True
  })

def web_parser(input):
  while True:
    print()

    material = input #input('What material?')

    if material.lower() == 'exit':
      break

    suppliers = SEARCH_PROVIDER.search(material)

    with open(
      'backend/web_parser/excluded_domains.json',
      encoding='utf-8'
    ) as f:
      
      excluded_domains = json.load(f)



    if not suppliers:
      return 'NOT FOUND'

    result = []

    for supplier in suppliers:
      domain = urlparse(supplier.url).netloc.lower()
      if any(excluded in domain for excluded in excluded_domains):
        continue
      pg_loaded = LOADER.load(supplier.url)
      if pg_loaded:
        # print(supplier.url)
        mails = EXTRACTOR.extract(supplier.url, pg_loaded).email
        mails = list(set(mails))
        if len(mails) == 0:
          continue
        result.append({
          'url': urlparse(supplier.url).netloc,
          'mail': mails
        })

    return result

@login_required
def parse_comp_page(request):
  return render(
    request,
    'companies/parse_comp_page.html',
    {
      
    }
  )

def parse_comp(request):
  parse_input = json.loads(request.body)['request_txt']
  results = []
  err = None
  try:
    results = web_parser(parse_input) #[f'url: {item['url']} - mail: {item['mail']}' for item in web_parser(parse_input)]
  except Exception as e:
    err = f"Ошибка: {e}"
    return JsonResponse({
      'success': False,
      'err_txt':err
    })

  return JsonResponse({
    'success': True,
    'results':results
  })