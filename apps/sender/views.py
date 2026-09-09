from django.http import JsonResponse
from django.utils import timezone

import openpyxl
import json

from apps.sender.sender_services import work_classifier, test_model
from apps.sender.models import TrainingExample

from backend.ai.ai_service import AiService

def sender(request):
  uploaded_files = request.FILES.getlist('files')

  for file in uploaded_files:
    print(file)
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active
    for row in sheet.iter_rows(values_only=True):
      print(row)

    workbook.close()

  return JsonResponse({
      'success': True
    })

def categorize(request):
  input_data = json.loads(request.body)
  categories = TrainingExample.objects.filter(label__isnull=False, status__in=['labeled', 'reviewed'])
  unique_categories = list(set([cat.label for cat in categories]))
  print(input_data)
  user_query = json.dumps({'work_name': input_data, 'categories': unique_categories}, ensure_ascii=False)
  output = AiService.execute_ai_query(system_query='Определи категорию work_name из списка categories. Верни ответ в формате "Работа: <work_name> \\nКатегорий: <category> \\nВероятность: <Уверенность в ответе в процентах>"', user_query=user_query) #test_model([input_data['input']])
  print(output)
  return JsonResponse({
    'success': True,
    'output': output 
  })

def label_category(request):
  input_data = json.loads(request.body)
  labeled_data = input_data['labeledData']

  for label in labeled_data:
    if label['label'] == 'delete':
      TrainingExample.objects.filter(id=label['id']).delete()
      continue
    item = TrainingExample.objects.filter(id=label['id'])
    item.update(label=label['label'], status='labeled', labeled_at = timezone.now(), labeled_by=None)

  return JsonResponse({
    'success': True
  })