from django.urls import path
from .views import sender, categorize, label_category

urlpatterns = [
  path('send_file/', sender),
  path('categorize/', categorize),
  path('label/', label_category)
]