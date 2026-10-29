from django.urls import path
from .views import CommonOperations, SpecialOperations
urlpatterns = [
  path('delete_connection/', CommonOperations.delete_connections),
  path('edit_connections/', CommonOperations.edit_connections),

  path('set_brend_list/', CommonOperations.create_brend_list),
  path('delete_brend_list_item/', CommonOperations.delete_from_brend_list),
  path('export_brend_list_excel/', SpecialOperations.export_brendlist_excel),

  path('add/', CommonOperations.create),

  path('edit/', CommonOperations.edit),
  path('delete/', CommonOperations.delete),


  path('create_Excel_Output/', SpecialOperations.create_Excel_Output),
  # path('parse_company/', SpecialOperations.parse_comp),
]