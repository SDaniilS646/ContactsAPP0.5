from django.shortcuts import render, redirect
from django.http import JsonResponse


from services.company_service import CompanyService
from services.material_service import MaterialService
from services.contact_service import ContactService
from services.connection_service import ConnectionService

from services.contact_service import ContactService

from django.utils import timezone


import json


from django.contrib.auth.decorators import login_required

from backend.web_parser.config import SEARCH_PROVIDER, LOADER, EXTRACTOR

from urllib.parse import urlparse

from datetime import datetime


@login_required
def companies_page(request):
  

  # web_parser()
  
  companies = CompanyService.get_companies()
  companies = companies.order_by('id')
  
  loaded_companies = []

  for comp in companies:
    loaded_companies.append({
      'id': comp.id,
      'name': comp.name,
      'inn': comp.inn,
      'phone': comp.phone,
      'mail': comp.mail,
      'comment': comp.comment,
      'materials': ' '.join([item.name for item in comp.materials.all()]),
      'is_old': True if (timezone.now().date() - comp.updated_at.date()).days > 365 else False,
      'updated_at': comp.updated_at
    })
    # print(datetime.strptime(comp.updated_at, "%Y-%m-%d").date())
  return render(
      request,
      'base.html',
      {
        'companies':loaded_companies
      }
  )
  return render(
    request,
    'companies/companies_page.html',
    {
      'companies':loaded_companies
    }
  )

@login_required
def add_company_view(request):
  # material_tree = MaterialService.get_material_tree()
  # contacts = ContactService.get_contacts()

  return render(
    request,
    'companies/add_comp.html',
    {
      # 'material_tree': material_tree,
      # 'contacts': contacts
    }
  )

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

@login_required
def company_details_page(request, id):
  company = CompanyService.get_company(id)

  comp_cont = ConnectionService.get_company_contact('company', id)
  comp_cont_ids = [item.contact_id for item in comp_cont]

  contacts = company.contacts.all()
  cont_info = []

  materials = None
  materials = company.materials.all()

  comp_mat_ids = [item.id for item in materials]

  material_tree = MaterialService.get_material_tree(comp_mat_ids)
  all_contacts = ContactService.get_contacts()

  contacts_list = []

  for cont in all_contacts:
    if cont.id in comp_cont_ids:
      temp = [{'corp_mail': item.mail, 'corp_phone': item.phone, 'position': item.position} for item in comp_cont if item.contact_id == cont.id][0]
      contacts_list.append({
        'id': cont.id,
        'first_name': cont.first_name,
        'last_name': cont.last_name,
        'patronymic': cont.patronymic,
        'phone': cont.phone,
        'mail': cont.mail,
        'selected': True,
        'corp_mail': temp['corp_mail'],
        'corp_phone': temp['corp_phone'],
        'position': temp['position']
      })
    else:
      contacts_list.append({
        'id': cont.id,
        'first_name': cont.first_name,
        'last_name': cont.last_name,
        'patronymic': cont.patronymic,
        'phone': cont.phone,
        'mail': cont.mail
      })

  for cont in contacts:
    temp_info = [item for item in comp_cont if item.contact_id == cont.id]
    cont_info.append({
      'contact_id': cont.id,
      'cont_name': f'{cont.last_name} {cont.first_name}',
      'position': temp_info[0].position,
      'phone': temp_info[0].phone,
      'mail':temp_info[0].mail
    })

  

  rating = company.rating
  if company.rating:
    rating = '★' * int(company.rating)
  

  return render(
    request,
    'companies/detail.html',
    {
      'company':company,
      'cont_info': cont_info,
      'materials': materials,
      'rating': rating,
      'material_tree': material_tree,
      'contacts': contacts_list
    }
  )

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