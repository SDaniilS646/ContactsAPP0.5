from django.urls import path
from .views import ContactOperations, MaterialOperations, EmployeeOperations, CompanyOperations, MeetingOperations #, delete #, contacts_page, , contact_details_page

urlpatterns = [
  # path('', contacts_page),

  path('contacts_list/', ContactOperations.contacts_list), 
  path('contacts/add_cont/', ContactOperations.contact_create),
  path('edit_cont/', ContactOperations.contact_edit),
  path('materials/add_mat/', MaterialOperations.material_create),
  path('employees/add_emp/', EmployeeOperations.employee_create),
  path('companies/add_comp/', CompanyOperations.company_create),
  path('meetings/add_meet/', MeetingOperations.meeting_create),
  # path('<int:id>/', contact_details_page),
  # path('delete/', delete)

]