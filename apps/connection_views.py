from .connection_models import CompaniesContacts, CompaniesMaterials
from django.http import JsonResponse
from apps.materials.views import check_material_children

import json

def delete_connection(request):
  data = json.loads(request.body)
  id_1 = data['id_1']
  id_2 = data['id_2']
  print(data)

  if data['table'] == 'company_contacts':
    # id_1 - cont, id_2 - comp
    CompaniesContacts.objects.filter(
      contact=id_1,
      company=id_2
    ).delete()
    
    return JsonResponse({
      'success': True
    })
  elif data['table'] == 'company_materials':
    # id_1 - mat, id_2 - comp

    CompaniesMaterials.objects.filter(
      materials=id_1,
      company=id_2
    ).delete()

    return JsonResponse({
      'success': True
    })