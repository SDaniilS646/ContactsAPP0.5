from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

# removeAllModals(); openModal('materials-details-modal-frame', 'detailsMaterial', {{material.material_id}})

NODE_CONFIG = {
  'page_style' : {
    'tag': "button",
    'onclick': "removeAllModals(); openModal('materials-details-modal-frame', 'detailsMaterial', {id})",
    'style': 'text-btn'
  },
  'material_creation' : {
    'tag': 'span',
    'onclick': 'selectParent(event, this)'
  },
  'material_editor' : {
    'tag': 'span',
    'onclick': "selectParent(event, this, 'edit_material_modal_frame')",
    'selected': lambda m, p: p and p.id == m['material_id']
  },
  'company_creation' : {
    'tag': 'span',
    'onclick': "selectMaterials(event, this, 'list_material_tree', 'materials-list-input-box')",
    'selected': lambda m, p: m['selected']
  }
}

@register.simple_tag
def material_node_tag(style, material, parent=None):
  cfg = NODE_CONFIG.get(style)

  if not cfg:
    return ''
  
  mat_id = material['material_id']

  css_style = cfg.get('style') if cfg.get('style') else ''
  selected = cfg.get('selected')
  selected = 'selected' if selected and selected(material, parent) else ''

  css_class = f'{css_style} {selected}'

  return format_html(
    '<{tag} id="{id}" class="{cls}" onclick="{onclick}">{name}</{tag}>', 
    tag=mark_safe(cfg['tag']), 
    id=mat_id,
    cls=css_class,
    onclick=mark_safe(cfg['onclick'].format(id=mat_id)),
    name=mark_safe(material['material_name'])
  )