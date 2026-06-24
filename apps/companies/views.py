from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse

from apps.companies.models import Companies
from apps.contacts.models import Contacts
from apps.connection_models import CompaniesContacts, CompaniesMaterials

import json

from apps.materials.views import get_material_tree
from apps.materials.models import Materials
from core.menu import MAIN_TABS

from django.contrib.auth.decorators import login_required

from datetime import datetime


@login_required
def companies_list(request):

  search = request.GET.get('search', '')
  search_type = request.GET.get('search_type')
  
  companies = Companies.objects.all()
  for company in companies:
    materials = company.materials.all()
    temp_mats = []
    for mat in materials:
      temp_mats.append(mat.name)
    company.mat = ";".join(temp_mats)


  today = datetime.now(timezone.UTC)

  for comp in companies:
    if (timezone.now().date() - comp.updated_at.date()).days < 15:
      comp.is_old = True

  if search:
    if search_type == 'mat':
      companies = companies.filter(
        materials__name__icontains=search
      )
    elif search_type == 'comp':
      companies = companies.filter(
        name__icontains=search
      )
    elif search_type == 'inn':
      companies = companies.filter(
        inn__icontains=search
      )

  return render(
    request,
    'companies/list.html',
    {
      'companies':companies,
      'active_page':'companies',
      'show_menu': True,
      'search': search,
      'search_type': search_type
    }
  )
  
def sort_contacts(contacts, all_contacts):
  old_contacts_ids = []
  for prev_cont in contacts:
    for idx, cont in enumerate(all_contacts):
      if prev_cont.id == cont.id:
        old_contacts_ids.append(idx)
        # print(idx)
        continue

  for idx in old_contacts_ids:
    temp = all_contacts.pop(idx)
    all_contacts.insert(0, temp)
    
  return all_contacts

def company_details(request, id):

  company = Companies.objects.get(id=id)
  print(company.email)
  all_contacts = list(Contacts.objects.all())
  

  contacts = company.contacts.all()
  materials = company.materials.all()

  contacts_ids = [item.id for item in contacts]

  materials_ids = [item.id for item in materials]

  
  all_contacts = sort_contacts(contacts, all_contacts)

  for cont in contacts:
    cont.pos = CompaniesContacts.objects.get(company=id, contact=cont.id).role_in_company

  for cont in all_contacts:
    if cont.id in contacts_ids:
      cont.pos = CompaniesContacts.objects.get(company=id, contact=cont.id).role_in_company

  err_list = None

  if request.method == 'POST':
    err, upd_data, upd_list, err_list = edit_company_check(request, company)
    print(err_list)
    if not err:
      for data in upd_list:
        Companies.objects.filter(id=id).update( **{data: upd_data[data]})
      Companies.objects.filter(id=id).update(updated_at=timezone.now())
      company = Companies.objects.get(id=id)

    print('posting')
  
  tree = get_material_tree(Materials.objects.all())

  return render(
    request, 
    'companies/detail.html', 
    {
      'company': company,
      'contacts': contacts,
      'contacts_ids': contacts_ids,
      'all_contacts': all_contacts,
      'materials': materials,
      'materials_ids': materials_ids,
      'show_cross': True,
      'cross_link': '/companies/',
      'rating': '' if not company.rating else ('★ ' * company.rating).strip(),
      'show_del': True,
      'del_base': 'comp',
      'del_id': id,
      'tree': tree,
      'error_values': err_list
    }
  )

def delete_company(request):
  data = json.loads(request.body)
  print('deleting')
  Companies.objects.filter(id=data['id']).delete()
  return JsonResponse({
    'success': True,
    'redirect_url': '/companies/'
  })

def upd_company_contacts(request):
  data = json.loads(request.body)
  comp_id = data['company_id']
  new_ids = data['contacts']

  old_ids = list(
    CompaniesContacts.objects
    .filter(company=comp_id)
    .values_list('contact', flat=True)
  )

  # if set(old_ids) == set(new_ids):
  #   print('nothing new')

  
  new_items = [{'id': item['id'], 'pos': item['pos'] } for item in new_ids if item['id'] not in old_ids]

  if len(new_items) > 0:
    for item in new_items:
      add_company_contact(
        {
          'company_id': Companies.objects.get(id=comp_id),
          'contact_id': Contacts.objects.get(id=item['id']),
          'position': item['pos']
        }
      )

  new_ids = [item['id'] for item in new_ids]
  removed_items = [item for item in old_ids if item not in new_ids]

  if len(removed_items) > 0:
    for item in removed_items:
      CompaniesContacts.objects.filter(company=comp_id, contact=item).delete()

  return JsonResponse({
    'success': True
  })

def company_create(request):
  contact_ids = []
  companies = Companies.objects.all()
  tree = get_material_tree(Materials.objects.all())

  if request.method == 'POST':

    is_error, values, error_values = new_company_check(request)

    

    if is_error:
      return render(
        request,
        'companies/add_comp.html',
        {
          'companies': companies,
          'tree': tree,

          'show_cross': True,
          'cross_link': '/companies/',
          
          'input_values': values,
          'error_values': error_values
        }
      )

    contacts = json.loads(
      request.POST.get(
        'contacts_json',
        '[]'
      )
    )

    company_id = add_new_company(request, values)

    if len(contacts) > 0:
      for contact in contacts:
        contact_ids.append(add_new_contact(contact=contact))

      for contact in contact_ids:
        addition_data = {
            'company_id': Companies.objects.get(id=company_id),
            'contact_id': Contacts.objects.get(id=contact[0]),
            'position': contact[1]
          }
        add_company_contact(addition_data)

    material_ids = request.POST.get(
      'materials_json'
    ).split(',')

    if len(material_ids) > 0:
      for mat_id in material_ids:
        addition_data= {
          'company_id': company_id,
          'material_id': mat_id,
        }
        add_company_materials(addition_data=addition_data)

    return redirect('/companies/')

  
  return render(
    request,
    'companies/add_comp.html',
    {
      'companies': companies,
      'tree': tree,
      'show_cross': True,
      'cross_link': '/companies/'
    }
  )

def add_new_company(request, values):
  input_data = request.POST
    
  new_company = Companies.objects.create(
    name=values['name'],
    inn=values['inn'],
    phone=input_data.get('phone'),
    email=input_data.get('mail'),
    website=input_data.get('website'),
    region=input_data.get('region'),
    rating=values['rating'],
    notes=input_data.get('comment'),
    created_at=timezone.now(),
    updated_at=timezone.now()
    )

  return new_company.id
  
def add_new_contact(request=None, contact=None):
  if not contact:
    if request:
      contact = json.loads(request.body)
      comp_id = contact['comp_id']

  new_contact = Contacts.objects.create(
    first_name = contact['first_name'],
    last_name = contact['last_name'],
    middle_name = contact['middle_name'],
    position = contact['position'],
    phone = contact['phone'],
    email = contact['mail'],
    created_at=timezone.now(),
    updated_at = timezone.now()
  )

  if request:

    add_company_contact(
      {
        'company_id': Companies.objects.get(id=comp_id),
        'contact_id': Contacts.objects.get(id=new_contact.id),
        'position': new_contact.position
      }
    )
    return JsonResponse({
      'success': True
    })

  return new_contact.id, new_contact.position

def add_company_contact(addition_data):

  CompaniesContacts.objects.create(
    company = addition_data['company_id'],
    contact = addition_data['contact_id'],
    role_in_company = addition_data['position'],
    created_at=timezone.now(),
    updated_at=timezone.now()
  )

def add_company_materials(request=None, addition_data=None):
  if not addition_data and request:
    data = json.loads(request.body)
    chosen_materials = data['materials']
    comp_id = data['comp_id']

    if len(chosen_materials) == 0:
      return JsonResponse({
      'success': False
    })
  elif addition_data:
    chosen_materials = [addition_data['material_id']]
    comp_id = addition_data['company_id']

  old_mats = list(
    CompaniesMaterials.objects.filter(company=comp_id).values_list('materials_id', flat=True)
  )
  print(old_mats)
  print(chosen_materials)

  new_mats = [item for item in chosen_materials if item not in old_mats]
  removed_mats = [item for item in old_mats if item not in chosen_materials]

  for item in removed_mats:
    CompaniesMaterials.objects.filter(company=comp_id, materials=item).delete()

  for mat_id in new_mats:
    CompaniesMaterials.objects.create(
      company = Companies.objects.get(id=comp_id),
      materials = Materials.objects.get(id=mat_id),
      created_at=timezone.now(),
      updated_at=timezone.now()
    )

  if request:
    return JsonResponse({
    'success': True
  })

def edit_company_check(request, old_data):
  input_data = request.POST
  updated_data = {}
  update_list = []

  error_values = {}

  error_list = []

  if input_data.get('name') != old_data.name:
    if input_data.get('name') != '':
      updated_data['name'] = input_data.get('name')
      update_list.append('name')
    else:
      error_values['name'] = 'Введите имя'
      error_list.append('name')

  if input_data.get('inn') != None and input_data.get('inn') != 'None' and input_data.get('inn') != old_data.inn:
    inn = input_data.get('inn')
    inn_list = list(Companies.objects.values_list('inn', flat=True))

    print(f'inn {type(inn)}')

    if inn and inn not in inn_list and len(inn) == 12:
      updated_data['inn'] = inn
      update_list.append('inn')
    else:
      if not inn or inn == 'None':
        updated_data['inn'] = None
        update_list.append('inn')
      elif inn in inn_list:
        error_values['inn'] = f'Такой инн уже есть - {'[ЗАГЛШКА]название компании'}'
        error_list.append('inn')
      elif len(inn) > 12:
        error_values['inn'] = 'Много цифр - должно быть 12'
        error_list.append('inn')
      elif len(inn) < 12:
        error_values['inn'] = 'Мало цифр - должно быть 12'
        error_list.append('inn')
      else:
        error_values['inn'] = 'Ошибка'
        error_list.append('inn')

  if int(input_data.get('rating')) != old_data.rating:
    rating = input_data.get('rating')
    if rating:
      try:
        if int(rating) not in range(0, 5):
          error_values['rating'] = 'Рейтинг должен быть от 0 до 5'
          error_list.append('rating')
        else:
          updated_data['rating'] = int(rating)
          update_list.append('rating')
      except:
        error_values['rating'] = 'Введите число от 0 до 5'
        error_list.append('rating')
    elif not rating or rating == '':
      updated_data['rating'] = None
      update_list.append('rating')
  
  if input_data.get('phone') != 'None' and input_data.get('phone') != old_data.phone:
    print(input_data.get('phone'))
    updated_data['phone'] = input_data.get('phone')
    update_list.append('phone')

  if input_data.get('mail') != 'None' and input_data.get('mail') != old_data.email:
    print(input_data.get('mail'))
    updated_data['email'] = input_data.get('mail')
    update_list.append('email')

  if input_data.get('website') != 'None' and input_data.get('website') != old_data.website:
    print(input_data.get('website'))
    updated_data['website'] = input_data.get('website')
    update_list.append('website')

  if input_data.get('region') != 'None' and input_data.get('region') != old_data.region:
    updated_data['region'] = None
    update_list.append('region')

  if input_data.get('comment') != 'None' and input_data.get('comment') != old_data.notes:
    print(input_data.get('comment'))
    updated_data['notes'] = input_data.get('comment')
    update_list.append('notes')


  if len(error_list) > 0:
    return True, updated_data, update_list, error_values
  elif len(error_list) == 0:
    return False, updated_data, update_list, error_values 

def new_company_check(request):
  input_data = request.POST
  values = {}

  error_values = {}

  error_list = []

  #===========================================
  # ПРОВЕРКА НАИМЕНОВАНИЯ
  #===========================================
  
  name  = input_data.get('name')
  if name == '':
    error_values['name'] = 'Введите имя'
    error_list.append('name')
  else:
    values['name'] = name

  #===========================================
  # ПРОВЕРКА ИНН
  #===========================================

  inn = input_data.get('inn')
  inn_list = list(Companies.objects.values_list('inn', flat=True))

  if inn and inn not in inn_list and len(inn) == 12:
    values['inn'] = inn
  else:
    if not inn:
      values['inn'] = None
    elif inn in inn_list:
      error_values['inn'] = f'Такой инн уже есть - {'[ЗАГЛШКА]название компании'}'
      error_list.append('inn')
    elif len(inn) > 12:
      error_values['inn'] = 'Много цифр - должно быть 12'
      error_list.append('inn')
    elif len(inn) < 12:
      error_values['inn'] = 'Мало цифр - должно быть 12'
      error_list.append('inn')
    else:
      error_values['inn'] = 'Ошибка'
      error_list.append('inn')

  #===========================================
  # ПРОВЕРКА РЕЙТИНГА
  #===========================================

  rating = input_data.get('rating')
  if rating:
    try:
      if int(rating) not in range(0, 5):
        error_values['rating'] = 'Рейтинг должен быть от 0 до 5'
        error_list.append('rating')
      else:
        values['rating'] = int(rating)
    except:
      error_values['rating'] = 'Введите число от 0 до 5'
      error_list.append('rating')
  elif not rating or rating == '':
    values['rating'] = None

  if len(error_list) > 0:
    return True, values, error_values
  elif len(error_list) == 0:
    return False, values, error_values