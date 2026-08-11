from django.urls import path
from .views import company_create, delete_connection, company_edit, edit_contact_list, delete, edit_material_list, parse_comp, parse_comp_page

urlpatterns = [
  path('add_comp/', company_create),
  path('edit_comp/', company_edit),
  path('delete_connection/', delete_connection),
  path('edit_contact_list/', edit_contact_list),
  path('edit_material_list/', edit_material_list),
  path('delete/', delete),
  path('parse_company_page/', parse_comp_page),
  path('parse_company/', parse_comp)
]

