from django.urls import path
from .views import contacts_list, contact_edit, delete #, contacts_page, contact_create, contact_details_page

urlpatterns = [
  # path('', contacts_page),

  path('contacts_list/', contacts_list), 
  # path('add_cont/', contact_create),
  path('edit_cont/', contact_edit),
  # path('<int:id>/', contact_details_page),
  path('delete/', delete)

]