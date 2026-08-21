from django.http import JsonResponse, HttpResponseBase, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test



from backend.web_parser.config import SEARCH_PROVIDER, LOADER, EXTRACTOR
from backend.xl_sender.sender_create import create_sendfile

from urllib.parse import urlparse

import json

from datetime import datetime
import shlex

from apps.crm.services.page_service import PageService, DetailService, AddService, ModalService
from apps.crm.services.model_services.contact_service import ContactService
from apps.crm.services.model_services.material_service import MaterialService
from apps.crm.services.model_services.employees_service import EmployeeService
from apps.crm.services.model_services.company_service import CompanyService
from apps.crm.services.model_services.meeting_service import MeetingService
from apps.crm.services.common_service import CommonService
from apps.crm.services.commands_service import Commands

from apps.crm.services.export_service import ExportService
from apps.crm.services.parser_service import WebParser

from apps.crm.services.model_services.connection_service import ConnectionService

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
  'createMeasure': ModalService.createMeasure,
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
  'chooseCompany': ModalService.chooseCompany,
  'listMeasure': ModalService.listMeasure,
  'editMeasure': ModalService.editMeasure
}

COMMANDS = {
  'help': Commands.HelpCommand,
  'all_users': Commands.getUsers,
  'create_user': Commands.createUser,
  'reset_password': Commands.resetPassword,
  'delete_user': Commands.deleteUser,
  'load_csv': Commands.getalldata,
  'check_con': Commands.checkConnections,
  'models': Commands.getModels,
  'sql': Commands.sqlQuery
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

class CommonOperations:
  def delete(request):
    input_data = json.loads(request.body)
    table_name = input_data.get('table')
    id = input_data.get('id')

    if not table_name or not id:
      return JsonResponse({
        'success': False,
        'errorType': 'type(e).__name__',
        'errorDescription': str(e),
        'error': f'no id ({id}) or table name ({table_name})'
      })

    try:
      CommonService.delete_item(table_name, id)
    except Exception as e:
      return JsonResponse({
        'success': False,
        'errorType': type(e).__name__,
        'errorDescription': str(e)
      })

    return JsonResponse({
      'success': True
    })

  def edit(request):
    input_data = json.loads(request.body)
    table_name = input_data.get('table')
    id = input_data.get('id')

    user = request.user

    if not table_name or not id:
      return JsonResponse({
        'success': False,
        'error': f'no id ({id}) or table name ({table_name})'
      })
    try:
      CommonService.edit(table_name, id, input_data, user)
    except Exception as e:
      return JsonResponse({
        'success': False,
        'errorType': type(e).__name__,
        'errorDescription': str(e)
      })
    
    return JsonResponse({
      'success': True
    })

  def create(request):
    input_data = json.loads(request.body)
    table_name = input_data.get('table')
    user = request.user

    try:
      new_id = CommonService.add(table_name, input_data, user)
    except Exception as e:
      print(e)
      return JsonResponse({
        'success': False,
        'errorType': type(e).__name__,
        'errorDescription': str(e)
      })
    
    return JsonResponse({
      'success': True,
      'new_id':new_id
    })

  def delete_connections(request):
    input_data = json.loads(request.body)
    print(input_data)

    user = request.user
    try:
      ConnectionService.delete_connection(input_data, user)
    except Exception as e:
      return JsonResponse({
        'success': False,
        'errorType': type(e).__name__,
        'errorDescription': str(e)
      })
    
    return JsonResponse({
      'success': True
    })

  def edit_connections(request):
    input_data = json.loads(request.body)
    user = request.user

    connection_data = {}
    connection_data['table1'] = input_data['table1']
    connection_data['table2'] = input_data['table2']
    connection_data['id1'] = input_data['id1']

    for item in input_data['connections']:
      connection_data['id2'] = item['id']
      extra = {key: value for key, value in item.items() if key != 'id'}
      connection_data['extra'] = extra
      ConnectionService.create_connection(connection_data, user)

    return JsonResponse({
      'success': True
    })

class SpecialOperations:
  def create_Excel_Output(request):
    try:
      payload = json.loads(request.body)
      companies_ids = payload['company_ids']
    except (json.JSONDecodeError, KeyError):
      return HttpResponseBadRequest(
        json.dumps({'success': False, 'error': 'Некорректны данные запроса'}),
        content_type='application/json'
      )
    output_data = ExportService.get_companies_output(companies_ids)

    buffer = create_sendfile(output_data)

    if buffer is None:
      return HttpResponseBadRequest(
        json.dumps({'success': False, 'error':  'Нет данных для экспорта'}), 
        content_type='application/json'
      )

    filename = f"sendfile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsm"
    response = HttpResponse(
      buffer.getvalue(),
      content_type='application/vnd.ms-excel.sheet.macroEnabled.12'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
      
    return response

  def parse_comp(request):
    parse_input = json.loads(request.body)['request_txt']
    results = []
    err = None
    try:
      results = WebParser.web_parser(parse_input) #[f'url: {item['url']} - mail: {item['mail']}' for item in web_parser(parse_input)]
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

class CommandOperations:
  def executeCMD(request):
    if not Commands.checkrole(request.user):
      return JsonResponse({
        'success': False,
        'res': 'Нет доступа'
      }, status=403)

    if request.method != 'POST':
      return JsonResponse({
        'success': False,
        'res': 'Метод не поддерживается'
      }, status=405)
    
    if request.content_type == 'application/json':
      full_cmd = json.loads(request.body)['command']
    else:
      full_cmd = request.POST['command']

    try:
      full_cmd = shlex.split(full_cmd)
    except ValueError as e:
      return JsonResponse({
        'success': False,
        'res': f'Ошибка разбора команды: {e}'
      }, status=400)
    
    if not full_cmd:
      return JsonResponse({
        'success': False,
        'res': 'Пустая команда'
      }, status=400)
    
    cmd = full_cmd[0]
    args = full_cmd[1:]

    handler = COMMANDS.get(cmd)
    if not handler:
      return JsonResponse({
        'success': False,
        'res': f'Неизвестная команда: {cmd}'
      }, status=400)

    try:
      res = handler(args)
    except Exception as e:
      return JsonResponse({
        'success': False,
        'res': f'Ошибка выполнения команнды: {e}'
      }, status=500)


    if isinstance(res, HttpResponseBase):
      return res
    
    return JsonResponse({
      'success': True,
      'res': res
    })


    input_data = json.loads(request.body)

    company_materials = input_data['company_materials']

    ConnectionService.delete_all_material_connections(input_data['id'])

    if company_materials:
      for material in company_materials:
        ConnectionService.edit_company_material(
          {
            'comp_id': input_data['id'],
            'mat_id': material,
            'user': request.user
          }
        )

    CommonService.item_update('companies', input_data['id'], request.user)

    return JsonResponse({
      'success': True
    })