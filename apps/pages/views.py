
from apps.pages.services.page_service import PageService, DetailService, AddService, ModalService
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import json

PAGES = {
  'companies': PageService.companies_page,
  'materials': PageService.materials_page,
  'contacts': PageService.contacts_page,
  'meetings': PageService.meetings_page,
  'employees': PageService.employees_page,
  'cmd': PageService.cmd_page,
  'parser': PageService.parser_page,
  'sender': PageService.sender_page, 
  'objects': PageService.objects_page,
  'aiConfig': PageService.ai_config_page
}

ADD = {
  'companies': AddService.addCompanyPage,
  'meetings': AddService.addMeetingPage
}

MODALS = {
  'createMaterial': ModalService.createMaterial,
  'createContact': ModalService.createContact,
  'createMeasure': ModalService.createMeasure,
  'createEmployee': ModalService.createEmployee,
  'createObject': ModalService.createObject,
  'chooseMaterial': ModalService.chooseMaterial,
  'chooseContact': ModalService.chooseContact,
  'chooseEmployee': ModalService.chooseEmployee,
  'editCompany': ModalService.editCompany,
  'editContact': ModalService.editContact,
  'editMaterial': ModalService.editMaterial,
  'editEmployee': ModalService.editEmployee,
  'editMeasure': ModalService.editMeasure,
  'editObject': ModalService.editObject,
  'detailsCompany': DetailService.companiesDetail,
  'detailsContact': DetailService.contactsDetail,
  'detailsMaterial': DetailService.materialsDetail,
  'detailsMeeting': DetailService.meetingsDetail,
  'detailsObjects': DetailService.objectsDetail,
  'detailsModel': DetailService.modelDetail,
  'chooseCompany': ModalService.chooseCompany,
  'chooseBrendList': ModalService.chooseBrendList,
  'listMeasure': ModalService.listMeasure,
  'activeLearningCaterories': ModalService.alCategories
}



@login_required
def clearPage(request):
  return render(request, 'base.html')

def setPage(request):
  page_data = json.loads(request.body)
  if page_data['type'] == 'page':
    html, vars = PAGES[page_data['table']]()
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