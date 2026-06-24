from django.urls import path
from .views import companies_list, company_details, company_create, delete_company, add_new_contact, add_company_materials, upd_company_contacts

urlpatterns = [
  path('', companies_list),

  path('<int:id>/', company_details),
  path('add_comp/', company_create),
  path('delete-companies/', delete_company),
  path('add_cont/', add_new_contact),
  path('add_mat_comp_connection/', add_company_materials),
  path('upd_company_contacts/', upd_company_contacts)
  # path('edit_company_info', editCompanyInfo)
  
]

