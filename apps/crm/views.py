from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

import json
import time

from datetime import datetime
from django.utils import timezone

from apps.crm.services.page_service import PageService, DetailService, AddService, ModalService
from apps.crm.services.contact_service import ContactService
from apps.crm.services.material_service import MaterialService
from apps.crm.services.employees_service import EmployeeService
from apps.crm.services.company_service import CompanyService
from apps.crm.services.meeting_service import MeetingService

from apps.crm.services.connection_service import ConnectionService

PAGES = {
  'companies': PageService.companies_page,
  'materials': PageService.materials_page,
  'contacts': PageService.contacts_page,
  'meetings': PageService.meetings_page,
  'employees': PageService.employees_page,
  'cmd': PageService.cmd_page,
  'parser': PageService.parser_page,
  'sender': PageService.sender_page
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
  'editContact': ModalService.editContact,
  'editMaterial': ModalService.editMaterial,
  'editEmployee': ModalService.editEmployee,
  'detailsCompany': DetailService.companiesDetail,
  'detailsContact': DetailService.contactsDetail,
  'detailsMaterial': DetailService.materialsDetail,
  'detailsMeeting': DetailService.meetingsDetail,
  'chooseCompany': ModalService.chooseCompany
}

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

class ContactOperations:
  @staticmethod
  def contacts_list(request):
    print('ГРУЗИМ СПИСОК')

    contacts = ContactService.get_contacts().order_by('-added_at')
    style = request.GET.get('style')
    is_meeting = request.GET.get('is_meeting')

    return render(
      request,
      'lists/contacts_list.html',
      {
        'contacts':contacts,
        'style': style,
        'meeting_create': is_meeting
      }
    )

  @staticmethod
  def contact_create(request):
    input_data = json.loads(request.body)

    new_id = ContactService.set_contact(input_data)

    return JsonResponse({
      'success': True,
      'cont_id':new_id
    })

  @staticmethod
  def contact_edit(request):
    input_data = json.loads(request.body)

    ContactService.edit_contact(input_data)

    ContactService.item_update(input_data['id'])

    return JsonResponse({
      'success': True
    })

class MaterialOperations:
  @staticmethod
  def material_create(request):
    input_data = json.loads(request.body)

    new_id = MaterialService.set_material(input_data)

    return JsonResponse({
      'success': True,
      'mat_id':new_id
    })

class EmployeeOperations:
  @staticmethod
  def employee_create(request):
    input_data = json.loads(request.body)

    new_id = EmployeeService.set_employee(input_data)

    return JsonResponse({
      'success': True
    })

class  MeetingOperations:
  @staticmethod
  def meeting_create(request):
    input_data = json.loads(request.body)

    if input_data['meeting_date']:
      input_data['meeting_date'] = datetime.strptime(input_data['meeting_date'], '%Y-%m-%d')
    else:
      input_data['meeting_date'] = timezone.now()

    meet_id = MeetingService.set_meeting(input_data)

    meeting_contacts = input_data['meeting_contacts']
    meeting_employees = input_data['meeting_employees']
    meeting_companies = input_data['meeting_companies']

    if meeting_contacts:
      for contact in meeting_contacts:
        ConnectionService.set_meeting_contact(
          {
            'meet_id': meet_id,
            'cont_id': contact['id']
          }
        )
    if meeting_employees:
      for employee in meeting_employees:
        ConnectionService.set_meeting_employee(
          {
            'meet_id': meet_id,
            'emp_id':employee['id']
          }
        )

    if meeting_companies:
      for company in meeting_companies:
        ConnectionService.set_meeting_company(
          {
            'meet_id': meet_id,
            'company_id':company['id']
          }
        )

    return JsonResponse({
      'success': True
    })

class CompanyOperations:
  @staticmethod
  def company_create(request):
    input_data = json.loads(request.body)

    old_companies = CompanyService.get_companies()
    comp_name = input_data['company_name']
    comp_mail = input_data['mail']

    old_companies_names = [item.name for item in old_companies]
    old_companies_mails = [item.mail for item in old_companies]

    if comp_name in old_companies_names or (comp_mail and comp_mail in old_companies_mails):
      return JsonResponse({
        'Success': False,
        'result': 'Exists'
      })

    input_data['user'] = request.user
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
            'cont_position': contact['position'],
            'user': request.user
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
            'mat_id': material,
            'user': request.user
          }
        )

    return JsonResponse({
      'success': True,
      'comp_name': comp_name,
      'comp_id':new_comp_id
    })