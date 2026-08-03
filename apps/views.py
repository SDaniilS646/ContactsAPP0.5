from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

import json
import time

from services.page_service import PageService, DetailService, AddService, ModalService

PAGES = {
  'companies': PageService.companies_page,
  'materials': PageService.materials_page,
  'contacts': PageService.contacts_page,
  'meetings': PageService.meetings_page,
  'employees': PageService.employees_page,
  'cmd': PageService.cmd_page
}

DETAILS = {
  'companies': DetailService.companiesDetail,
  'materials': DetailService.materialsDetail,
  'contacts': DetailService.contactsDetail,
  'meetings': DetailService.meetingsDetail,
  'employees': DetailService.employeesDetail
}

ADD = {
  'companies': AddService.addCompanyPage,
  'meetings': AddService.addMeetingPage
}

MODALS = {
  'createMaterial': ModalService.createMaterial,
  'createContact': ModalService.createContact,
  'createEmployee': ModalService.createEmployee,
  'chooseMaterial': ModalService.chooseMaterial,
  'chooseContact': ModalService.chooseContact,
  'chooseEmployee': ModalService.chooseEmployee,
  'editCompany': ModalService.editCompany,
  'detailsCompany': DetailService.companiesDetail
}

@login_required
def clearPage(request):
  return render(request, 'base.html')

def setPage(request):
  page_data = json.loads(request.body)

  if page_data['type'] == 'page':
    html, vars = PAGES[page_data['table']]()
  elif page_data['type'] == 'details':
    html, vars = DETAILS[page_data['table']](page_data['id'])
  elif page_data['type'] == 'add':
    html, vars = ADD[page_data['table']]()
  else:
    return JsonResponse({'success': False})


  return JsonResponse({
    'success': True,
    'result': 'Exists',
    'html': render_to_string(
      html, vars, request=request)
  })

def loadModal(request):
  page_data = json.loads(request.body)
  
  html, vars = MODALS[page_data['modal_name']](page_data['id'])

  return JsonResponse({
    'html': render_to_string(html, vars, request=request)
  })

