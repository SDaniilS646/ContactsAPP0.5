from django.http import JsonResponse

import openpyxl
import json

from apps.sender.sender_services import work_classifier, test_model

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