from django.http import JsonResponse
from django.utils import timezone

import openpyxl
import json

from apps.sender.sender_services import work_classifier, test_model

from apps.sender.models import TrainingExample

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
  output = test_model([input_data['input']])
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