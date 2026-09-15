from django.urls import path
from .views import sender, categorize, label_category, execute_ai

urlpatterns = [
  path('send_file/', sender),
  path('categorize/', categorize),
  path('label/', label_category),

  path('ai_request/', execute_ai)
]