from django.shortcuts import render
from django.http import JsonResponse
from .models import Contacts
from apps.companies.models import Companies
from apps.connection_models import CompaniesContacts

import json
import re

def contacts_list(request):
  contacts = Contacts.objects.all()

  for cont in contacts:
      
    temp_phone = cont.phone
    if not temp_phone:
      continue
    

    if temp_phone.startswith('+7'):
      temp_phone = temp_phone.replace('+7', '8')
    temp_phone = temp_phone.replace(' ', '')

    temp_phone = re.sub(r'[()-]', '', temp_phone)

    cont.phone = temp_phone

  return render(
    request,
    'contacts/list.html',
    {
      'contacts':contacts,
      'active_page':'contacts',
      'show_menu': True,
      }
    )

def contact_details(request, id):
  
  contact = Contacts.objects.get(id=id)
  companies = contact.companies.all()
  companies.order_by('id')
  comp_cont = CompaniesContacts.objects.filter(contact=id)
  comp_cont.order_by('company')

  comp_info = []

  for idx, company in enumerate(companies):
    print(company.name)
    print(comp_cont[idx].role_in_company)
    comp_info.append({
      'name': company.name,
      'role': comp_cont[idx].role_in_company,
      'comp_id': company.id,
      'cont_id': id
    })
  

  return render(
    request, 
    'contacts/detail.html', 
    {
      'contact': contact,
      'companies': companies,
      'roles': comp_cont,
      'comp_info': comp_info,
      'show_cross': True,
      'cross_link': '/contacts/',
      'show_del': True,
      'del_base': 'cont',
      'del_id': id
    }
  )

def delete_company(request):
  data = json.loads(request.body)
  print('deleting')
  Contacts.objects.filter(id=data['id']).delete()
  print(f'delted {data['id']}')
  return JsonResponse({
    'success': True,
    'redirect_url': '/contacts/'
  })