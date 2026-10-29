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

  @login_required
  def get_information(request):
    if not request.user.is_superuser:
      return JsonResponse({'success':False})
    input_data = json.loads(request.body)
    output = AiService.get_version_info(input_data['id'])
    return JsonResponse({
      'success': True,
      'output': output
    })

  @login_required
  def create_version(request):
    if not request.user.is_superuser:
      return JsonResponse({'success':False})
    input_data = json.loads(request.body)
    AiService.create_version(input_data)
    return JsonResponse({'success':True})

  @login_required
  def activate_version(request):
    if not request.user.is_superuser:
      return JsonResponse({'success':False})
    input_data = json.loads(request.body)
    AiService.activate(input_data['id'])
    return JsonResponse({
      'success': True
    })

  @login_required
  def label_material(request):
    input_data = json.loads(request.body)
    AiService.save_material_label(input_data.get('labeledData'))
    # AiService.prepare_dpo_dataset()
    return JsonResponse({
      'success': True
    })