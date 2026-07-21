from django.urls import path
from .views import commands_page, executeCMD

urlpatterns = [
  path('', commands_page),
  path('executeCMD/', executeCMD),
]
