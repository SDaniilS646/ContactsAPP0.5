from django.shortcuts import render
from django.http import JsonResponse
from apps.crm.services.employees_service import EmployeeService
from apps.crm.services.connection_service import ConnectionService
from django.contrib.auth.decorators import login_required

from django.utils import timezone

import json

@login_required
def employees_page(request):
  employees = EmployeeService.get_employees()
  employees = employees.order_by('last_name')
  loaded_contacts = []

  return

  return render(
    request,
    'employees/employees_page.html',
    {
      'employees':employees,
      'style': 'cards'
      }
    )

def employees_list(request):
  print('ГРУЗИМ СПИСОК')

  employees = EmployeeService.get_employees().order_by('-added_at')
  style = request.GET.get('style')

  return render(
    request,
    'lists/employees_list.html',
    {
      'employees':employees,
      'style': style
    }
  )

def employee_create(request):
  input_data = json.loads(request.body)

  new_id = EmployeeService.set_employee(input_data)

  return JsonResponse({
    'success': True
  })

def employee_edit(request):
  input_data = json.loads(request.body)

  EmployeeService.edit_employee(input_data)

  EmployeeService.item_update(input_data['id'])

  return JsonResponse({
    'success': True
  })

@login_required
def employee_details_page(request, id):
  employee = EmployeeService.get_employee(id)
  emp_info = [] # ConnectionService.get_company_contact('contact', id)

  return render(
    request,
    'employees/detail.html',
    {
      'employee':employee,
      'emp_info':emp_info
    }
  )

def delete(request):
  input_data = json.loads(request.body)

  EmployeeService.delete(input_data['id'])

  return JsonResponse({
    'success': True
  })