from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
import json
from .models import Materials
from apps.connection_models import CompaniesMaterials

def get_material_tree(materials):
  nodes = {}
  for material in materials:
    nodes[material.id] = {
      'id': material.id,
      'name': material.name,
      'parent_id': material.parent_id if material.parent_id else 'none',
      'children': []
    }

  tree = []

  for material in materials:
    node = nodes[material.id]

    if material.parent_id:
      nodes[material.parent_id]['children'].append(node)
    else:
      tree.append(node)

  return tree

def materials_list(request):
  materials = Materials.objects.all().order_by('-parent_id', 'id')

  tree = get_material_tree(materials)

  return render(
    request,
    'materials/list.html',
    {
      'tree': tree,
      'materials':materials,
      'active_page':'materials',
      'show_menu': True,
      }
    )


def check_material_parent(id):
  material = Materials.objects.get(id=id)
  materials = Materials.objects.all()

  temp_par_id = material.parent_id
  if not temp_par_id:
    return None

  idx = 0
  par_list = []

  while temp_par_id:
    for temp_material in materials:
      if temp_material.id == temp_par_id:
        par_list.insert(0,
          {
            'id': temp_material.id,
            'parent_id': temp_material.parent_id,
            'name': temp_material.name
          }
        )
        temp_par_id = temp_material.parent_id
        break
    idx = idx + 1
    if idx > 1000:
      print('BREAKING WHILE LOOP!!!')
      return None

  return par_list

def check_material_children(id):
  material = Materials.objects.get(id=id)
  materials = Materials.objects.all().order_by('name')

  par_ids = list(
    Materials.objects.values_list(
      'parent_id',
      flat=True
    )
  )

  if material.id not in par_ids:
    return None

  children = []

  for temp_material in materials:
    if temp_material.parent_id == id:
      children.append(
        {
          'name': temp_material.name,
          'id': temp_material.id
        }
      )

  return children

def material_details(request, id):
  
  material = Materials.objects.get(id=id)
  keywords = ','.join(material.keywords)

  companies = material.companies.all()
  companies.order_by('id')
  
  parents = None
  children = None

  parents = check_material_parent(id)
  
  children = check_material_children(id)

  tree = get_material_tree(Materials.objects.all())

  return render(
    request, 
    'materials/detail.html', 
    {
      'material': material,
      'companies': companies,
      'keywords': keywords,
      'parents': parents,
      'children': children,
      'show_cross': True,
      'cross_link': '/materials/',
      'show_del': True,
      'del_base': 'mat',
      'del_id': id,
      'tree': tree
    }
  )

def material_create(request):
  data = json.loads(request.body)

  temp_keywords = data['keywords'].split(',')

  if data['is_edit']:
    Materials.objects.filter(id=data['id']).update(
      name=data['name'],
      keywords=temp_keywords,
      parent_id=data['parent_id'],
      updated_at=timezone.now()
    )
    return JsonResponse({'success': True, 'is_edit': True})
  
  
  new_material = Materials.objects.create(
    name=data['name'],
    keywords=temp_keywords,
    parent_id=data.get('parent_id') or None,
    created_at=timezone.now(),
    updated_at=timezone.now()
  )

  return JsonResponse({
    'id': new_material.id,
    'name': new_material.name,
    'is_edit': False
  })

def materials_tree(request):
  tree = get_material_tree(Materials.objects.all())
  modal_task = request.GET.get('modal_task')

  if modal_task == 'new_mat':
    return render(
      request,
      'components/mat_tree.html',
      {
        'tree':tree,
        'modal_task': modal_task
      }
    )
  
  return render(
    request,
    'components/mat_tree.html',
    {
      'tree':tree,
      'modal_task': modal_task
    }
  )

def child_up(children, parent_id):
  for child in children:
    Materials.objects.filter(id=child['id']).update(
      parent_id=parent_id
    )

def delete_material(request):
  data = json.loads(request.body)
  children = check_material_children(data['id'])
  
  if children:
    parent_id = Materials.objects.get(id=data['id']).parent_id
    child_up(children, parent_id)
  
  Materials.objects.filter(id=data['id']).delete()
  return JsonResponse({
    'success': True,
    'redirect_url': '/materials/'
  })