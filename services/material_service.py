from apps.materials.models import Materials
from django.utils import timezone

class MaterialService:
  @staticmethod
  def get_materials():
    return Materials.objects.all()
  
  @staticmethod
  def set_material(input_data):
    new_id = Materials.objects.create(
      name = input_data['material_name'],
      parent_id = input_data['parent_id'],
      keywords = input_data['keywords'],
      updated_at = timezone.now(),
      added_at = timezone.now()
    ).id
    return new_id
  
  @staticmethod
  def get_material(mat_id):
    return Materials.objects.get(id=mat_id)
  
  @staticmethod
  def item_update(mat_id):
    Materials.objects.filter(id=mat_id).update(updated_at = timezone.now())
    return
  
  @staticmethod
  def get_material_tree(old_mats = []):
    materials = Materials.objects.all()
    def create_tree(materials):
        # materials = materials.order_by('-parent_id')
        nodes = {}
        material_tree = []

        for material in materials:
          nodes[material.id] = {
            'material_id': material.id,
            'material_name': material.name,
            'parent_id': material.parent_id,
            'children': [],
            'selected': True if material.id in old_mats else False
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
    return Materials.objects.get(id=par_id)
  
  @staticmethod
  def get_children(mat_id):
    return Materials.objects.filter(parent_id=mat_id)
  
  @staticmethod
  def edit_material(input_data):
    mat_id = input_data['id']
    Materials.objects.filter(id=mat_id).update(
      name = input_data['material_name'],
      parent_id = input_data['parent_id'],
      keywords = input_data['keywords'],
      updated_at = timezone.now()
    )
    return
  
  @staticmethod
  def getAllParents(mat_id):
    result = []
    material = Materials.objects.get(id=mat_id)
    
    def get_parent(mat_id):
      material = Materials.objects.get(id=mat_id)
      # parent = Materials.objects.get(id=material.parent_id)
      
      if material.parent_id:
        result.append(material.parent_id)
        get_parent(material.parent_id)

    if material.parent_id:
      get_parent(mat_id)
    else:
      result.append(mat_id)
    return result[::-1]

  @staticmethod
  def getAllChildren(mat_id, all_materials):
    result = []
    id = mat_id
    
    def findChildren(par_id):
      for mat in all_materials:
        if mat.parent_id == par_id:
          result.append(mat.id)
          findChildren(mat.id)

    findChildren(id)
    return result
      
  @staticmethod
  def delete(id):
    Materials.objects.filter(id=id).delete()
    return

    
    