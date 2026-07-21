from django.urls import path
from .views import employees_page, employee_create, employees_list, employee_details_page, delete, employee_edit

urlpatterns = [
  path('', employees_page),

  path('add_emp/', employee_create),
  path('employees_list/', employees_list),
  path('<int:id>/', employee_details_page),
  path('edit_emp/', employee_edit),

  path('delete/', delete)
]