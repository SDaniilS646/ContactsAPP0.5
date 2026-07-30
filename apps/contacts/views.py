from django.shortcuts import render
from django.http import JsonResponse
from services.contact_service import ContactService
from services.connection_service import ConnectionService

from django.contrib.auth.decorators import login_required

from django.utils import timezone

import json

@login_required
def contacts_page(request):
  contacts = ContactService.get_contacts()
  contacts = contacts.order_by('last_name')
  loaded_contacts = []

  for cont in contacts:
    loaded_contacts.append({
      'id': cont.id,
      'first_name': cont.first_name,
      'last_name': cont.last_name,
      'patronymic': cont.patronymic,
      'phone': cont.phone,
      'mail': cont.mail,
      'comment':cont.comment,
      'is_old': True if (timezone.now().date() - cont.updated_at.date()).days > 365 else False,
      'updated_at': cont.updated_at
    })

  return render(
        request,
        'base.html',
        {
          'contacts':loaded_contacts
        }
    )

  return render(
    request,
    'contacts/contacts_page.html',
    {
      'contacts':loaded_contacts
      }
    )

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

def contact_create(request):
  input_data = json.loads(request.body)

  new_id = ContactService.set_contact(input_data)

  return JsonResponse({
    'success': True,
    'cont_id':new_id
  })

def contact_edit(request):
  input_data = json.loads(request.body)

  ContactService.edit_contact(input_data)

  ContactService.item_update(input_data['id'])

  return JsonResponse({
    'success': True
  })

@login_required
def contact_details_page(request, id):
  contact = ContactService.get_contact(id)
  comp_cont = ConnectionService.get_company_contact('contact', id)

  companies = contact.companies.all()

  comp_info = []

  for company in companies:
    temp_info = [item for item in comp_cont if item.company_id == company.id]
    comp_info.append({
      'company_id': company.id,
      'company_name': company.name,
      'position': temp_info[0].position,
      'phone': temp_info[0].phone,
      'mail':temp_info[0].mail
    })

  return render(
    request,
    'contacts/detail.html',
    {
      'contact':contact,
      'comp_info':comp_info
    }
  )

def delete(request):
  input_data = json.loads(request.body)

  ContactService.delete(input_data['id'])

  return JsonResponse({
    'success': True
  })