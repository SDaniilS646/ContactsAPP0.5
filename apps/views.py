from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

import json

from services.page_service import PageService, DetailService

PAGES = {
  'companies': PageService.companies_page,
  'materials': PageService.materials_page,
  'contacts': PageService.contacts_page,
  'meetings': PageService.meetings_page,
  'employees': PageService.employees_page
}

DETAILS = {
  'companies': DetailService.companiesDetail,
  'materials': DetailService.materialsDetail,
  'contacts': DetailService.contactsDetail,
  'meetings': DetailService.meetingsDetail,
  'employees': DetailService.employeesDetail
}

ADD = {}

@login_required
def clearPage(request):
  return render(request, 'base.html')

def setPage(request):
  page_data = json.loads(request.body)

  if page_data['type'] == 'page':
    html, vars = PAGES[page_data['table']]()
  elif page_data['type'] == 'details':
    html, vars = DETAILS[page_data['table']](page_data['id'])
  elif page_data['type'] == 'ADD':
    ADD[page_data['table']]()
  else:
    print('missing type')


  return JsonResponse({
    'Success': False,
    'result': 'Exists',
    'html': render_to_string(
      html, vars)
  })