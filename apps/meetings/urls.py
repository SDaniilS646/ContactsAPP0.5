from django.urls import path
from .views import  meeting_create, delete
# , meetings_page, meeting_details_page, add_meeting_view

urlpatterns = [
  # path('', meetings_page),
  # path('add_meet_view/', add_meeting_view),
  path('add_meet/', meeting_create),
  # path('<int:id>/', meeting_details_page),
  path('delete/', delete)
]