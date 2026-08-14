from django.urls import path
from .views import sender

urlpatterns = [
  path('send_file/', sender)
]