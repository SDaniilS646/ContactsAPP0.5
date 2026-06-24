from django.urls import path
from .views import contacts_list, delete_company, contact_details

urlpatterns = [
  path('', contacts_list),
  path('delete_contacts/', delete_company),

  path('<int:id>/', contact_details),
  # path('create/', contact_create)
]