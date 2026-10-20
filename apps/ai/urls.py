from django.urls import path
from .views import AiOperations

urlpatterns = [
  path('version_info/', AiOperations.get_information),
  path('activate_version/', AiOperations.activate_version),
  path('create_version/', AiOperations.create_version),
  path('label_material/', AiOperations.label_material)
]