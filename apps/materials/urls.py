from django.urls import path
from .views import materials_page, material_create, materials_list, material_details_page, material_edit, delete

urlpatterns = [
  path('', materials_page),

  path('materials_list/', materials_list),
  path('add_mat/', material_create),
  path('edit_mat/', material_edit),
  path('<int:material_id>/', material_details_page),
  path('delete/', delete)
]