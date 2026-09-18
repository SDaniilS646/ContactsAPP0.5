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

  def activate_version(request):
    input_data = json.loads(request.body)
    AiService.activate(input_data['id'])
    return JsonResponse({
      'success': True
    })