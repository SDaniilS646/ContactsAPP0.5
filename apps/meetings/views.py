from django.shortcuts import render
from django.http import JsonResponse
from services.meeting_service import MeetingService

from services.contact_service import ContactService

from services.employees_service import EmployeeService

from services.connection_service import ConnectionService

from datetime import datetime

from django.utils import timezone

from django.contrib.auth.decorators import login_required

import json

@login_required
def meetings_page(request):
  meetings = MeetingService.get_meetings()

  return render(
    request,
    'meetings/meetings_page.html',
    {
      'meetings':meetings
    }
  )

@login_required
def add_meeting_view(request):
  # material_tree = MaterialService.get_material_tree()
  # contacts = ContactService.get_contacts()

  contacts = ContactService.get_contacts()
  employees = EmployeeService.get_employees()

  return render(
    request,
    'meetings/add_meeting.html',
    {
      'contacts': contacts,
      'employees': employees,
      'meeting_create': True
    }
  )


def meeting_create(request):
  input_data = json.loads(request.body)

  if input_data['meeting_date']:
    input_data['meeting_date'] = datetime.strptime(input_data['meeting_date'], '%Y-%m-%d')
  else:
    input_data['meeting_date'] = timezone.now()

  meet_id = MeetingService.set_meeting(input_data)

  meeting_contacts = input_data['meeting_contacts']
  meeting_employees = input_data['meeting_employees']

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

  return JsonResponse({
    'success': True
  })

@login_required
def meeting_details_page(request, id):
  meeting = MeetingService.get_meeting(id)

  contacts = meeting.contacts.all()
  employees = meeting.employees.all()

  return render(
    request,
    'meetings/detail.html',
    {
      'meeting':meeting,
      'contacts': contacts,
      'employees': employees
    }
  )

def delete(request):
  input_data = json.loads(request.body)

  MeetingService.delete(input_data['id'])

  return JsonResponse({
    'success': True
  })