from django.urls import path
from .views import meetings_page, add_meeting_view, meeting_create, meeting_details_page, delete

urlpatterns = [
  path('', meetings_page),
  path('add_meet_view/', add_meeting_view),
  path('add_meet/', meeting_create),
  path('<int:id>/', meeting_details_page),
  path('delete/', delete)
]