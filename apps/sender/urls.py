from django.urls import path
from .views import sender, categorize

urlpatterns = [
  path('send_file/', sender),
  path('categorize/', categorize)
]