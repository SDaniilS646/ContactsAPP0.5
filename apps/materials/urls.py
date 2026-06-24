from django.urls import path
from .views import materials_list, material_create, material_details, materials_tree, delete_material

urlpatterns = [
  path('', materials_list),

  path('<int:id>/', material_details),
  path('add_mat/', material_create),
  path('modal_frames/', materials_tree),
  path('delete-materials/', delete_material)
]