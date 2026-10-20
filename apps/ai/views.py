from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from apps.ai.services.ai_services import AiService

import json

class AiOperations:
  def test(request):
    return JsonResponse({
      'success': True
    })

  def get_information(request):
    input_data = json.loads(request.body)
    output = AiService.get_version_info(input_data['id'])
    return JsonResponse({
      'success': True,
      'output': output
    })
  
  def create_version(request):
    input_data = json.loads(request.body)
    AiService.create_version(input_data)
    return JsonResponse({'success':True})
  
  def activate_version(request):
    input_data = json.loads(request.body)
    AiService.activate(input_data['id'])
    return JsonResponse({
      'success': True
    })

  def label_material(request):
    input_data = json.loads(request.body)
    AiService.save_material_label(input_data.get('labeledData'))
    # AiService.prepare_dpo_dataset()
    return JsonResponse({
      'success': True
    })