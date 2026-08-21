from ...models.models import Material, Measure
from django.utils import timezone

from collections import defaultdict

class MeasureService:
  @staticmethod
  def create(input_data, user):
    new_id = Measure.objects.create(
      name = input_data['name'],
      title = input_data['title'],
    ).id
    return new_id

  @staticmethod
  def get_measures():
    return Measure.objects.all()
  
  @staticmethod
  def get_measure(id):
    return Measure.objects.filter(id=id).first()

  @staticmethod
  def edit(item, input_data):
    item.update(
      name = input_data['name'],
      title = input_data['title']
    )
    return
  
class MaterialService:
  @staticmethod
  def get_materials():
    return Material.objects.all()
  
  @staticmethod
  def create(input_data, user):
    new_id = Material.objects.create(
      name = input_data['material_name'],
      parent = MaterialService.get_material(mat_id=input_data['parent_id']),
      keywords = input_data['keywords'],
      measure = MeasureService.get_measure(id=input_data['measure_id'])
    ).id
    return new_id

  @staticmethod
  def get_material(mat_id):
    return Material.objects.filter(id=mat_id).first()
  
  @staticmethod
  def item_update(mat_id):
    Material.objects.filter(id=mat_id).update(updated_at = timezone.now())
    return
  
  @staticmethod
  def get_material_tree(materials=None, old_mats=None):
    old_mats = old_mats or []
    old_mats_set = set(old_mats)

    if not materials:
      materials = Material.objects.all()

    def create_tree(materials):
        nodes = {}
        material_tree = []

        for material in materials:
          nodes[material.id] = {
            'material_id': material.id,
            'material_name': material.name,
            'parent_id': material.parent_id,
            'measure': material.measure,
            'children': [],
            'selected': material.id in old_mats_set
          }

        for material in materials:
          node = nodes[material.id]

          if material.parent_id:
            nodes[material.parent_id]['children'].append(node)
          else:
            material_tree.append(node)

        return material_tree

    material_tree = create_tree(materials)

    return material_tree

  @staticmethod
  def get_parent(par_id):
    return Material.objects.get(id=par_id)
  
  @staticmethod
  def get_children(mat_id):
    return Material.objects.filter(parent=mat_id)
  
  @staticmethod
  def edit(item, input_data):
    item.update(
      name = input_data['material_name'],
      parent = input_data['parent_id'],
      keywords = input_data['keywords']
    )
    return
  
  @staticmethod
  def getAllParents(mat_id):
    result = []
    material = Material.objects.get(id=mat_id)
    
    def get_parent(mat_id):
      material = Material.objects.get(id=mat_id)
      
      if material.parent_id:
        result.append(material.parent_id)
        get_parent(material.parent_id)

    if material.parent_id:
      get_parent(mat_id)
    else:
      result.append(mat_id)
    return result[::-1]

  @staticmethod
  def getAllChildren(material_id, materials):
    children_by_parent = defaultdict(list)
    for material in materials:
      children_by_parent[material.parent_id].append(material.id)

    descendant_ids = []
    stack = list(children_by_parent[material_id])
    while stack:
      child_id = stack.pop()
      descendant_ids.append(child_id)
      stack.extend(children_by_parent[child_id])
    return descendant_ids
      

    
    