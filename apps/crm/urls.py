from django.urls import path
from .views import CommonOperations, CommandOperations, SpecialOperations
urlpatterns = [
  path('delete_connection/', CommonOperations.delete_connections),
  path('edit_connections/', CommonOperations.edit_connections),

  path('add/', CommonOperations.create),

  path('edit/', CommonOperations.edit),
  path('delete/', CommonOperations.delete),

  path('executeCMD/', CommandOperations.executeCMD),
  path('create_Excel_Output/', SpecialOperations.create_Excel_Output),
  path('parse_company/', SpecialOperations.parse_comp),
]