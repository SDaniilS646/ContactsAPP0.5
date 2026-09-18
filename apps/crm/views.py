from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from backend.xl_sender.sender_create import create_sendfile

import json

from datetime import datetime


from apps.pages.services.page_service import PageService, DetailService, AddService, ModalService
from apps.crm.services.common_service import CommonService

from apps.crm.services.export_service import ExportService
from apps.crm.services.parser_service import WebParser

from apps.crm.services.model_services.connection_service import ConnectionService


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

  def create_brend_list(request):
    input_data = json.loads(request.body)
    ConnectionService.create_brend_list(input_data, request.user)
    return JsonResponse({
      'success': True
    })

  def delete_from_brend_list(request):
    input_data = json.loads(request.body)
    ConnectionService.delete_from_brend_list(input_data)
    return JsonResponse({
      'success': True
    }) 

class SpecialOperations:
  def export_brendlist_excel(request):
    payload = json.loads(request.body)
    output = ExportService.get_object_brend_list(payload['object_id'])

    response = HttpResponse(
      output.getvalue(),
      content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = (
      'attachment; filename="brend_list.xlsx"'
    )
    return response

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

