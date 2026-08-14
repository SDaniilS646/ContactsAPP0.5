import json
from django.http import JsonResponse

import openpyxl

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