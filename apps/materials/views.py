from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
import json
from services.material_service import MaterialService
from apps.connection_models import CompanyMaterial

from django.contrib.auth.decorators import login_required

@login_required
def materials_page(request):
  materials = MaterialService.get_materials()

  material_tree = MaterialService.get_material_tree()

  return render(
    request,
    'materials/materials_page.html',
    {
      'materials':materials,
      'material_tree': material_tree
    }
  )

def materials_list(request):
  material_tree = MaterialService.get_material_tree()
  style = request.GET.get('style')
  return render(
    request,
    'lists/materials_list.html',
    {
    'material_tree': material_tree,
    'style': style
    }
  )

def material_create(request):
  input_data = json.loads(request.body)

  new_id = MaterialService.set_material(input_data)

  return JsonResponse({
    'success': True,
    'mat_id':new_id
  })

@login_required
def material_details_page(request, material_id):
  material = MaterialService.get_material(material_id)
  material_tree = MaterialService.get_material_tree()

  materials = MaterialService.get_materials()

  parent = None
  children = None
  companies = None

  if material.parent_id:
    parent = MaterialService.get_parent(material.parent_id)

  children = MaterialService.get_children(material_id)
  companies = material.companies.all()

  all_children = MaterialService.getAllChildren(material_id, materials)

  return render(
    request,
    'materials/detail.html',
    {
      'this_material':material,
      'parent': parent,
      'children': children,
      'companies': companies,
      'material_tree': material_tree,
      'all_children': all_children
    }
  )

def material_edit(request):
  input_data = json.loads(request.body)

  MaterialService.edit_material(input_data)

  MaterialService.item_update(input_data['id'])

  return JsonResponse({
    'success': True
  })


def delete(request):
  input_data = json.loads(request.body)

  MaterialService.delete(input_data['id'])

  return JsonResponse({
    'success': True
  })