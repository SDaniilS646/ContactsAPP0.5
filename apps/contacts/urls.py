from django.urls import path
from .views import contacts_page, contact_create, contacts_list, contact_details_page, contact_edit, delete

urlpatterns = [
  path('', contacts_page),

  path('contacts_list/', contacts_list), 
  path('add_cont/', contact_create),
  path('edit_cont/', contact_edit),
  path('<int:id>/', contact_details_page),
  path('delete/', delete)

]