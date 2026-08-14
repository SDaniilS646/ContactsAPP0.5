from django.contrib.auth.models import User
from django.apps import apps
from django.http import FileResponse
from django.db import connection

from apps.companies.models import Companies
from apps.contacts.models import Contacts
from apps.materials.models import Materials
from apps.meetings.models import Meetings
from apps.employees.models import Employees
from apps.connections.models import CompanyContact, CompanyMaterial, MeetingContact, MeetingEmployee

from pathlib import Path

import csv
import io
import zipfile
from datetime import datetime

MODELS = {
  'companies': Companies,
  'contacts': Contacts,
  'meetings': Meetings,
  'materials': Materials,
  'employees': Employees,
  'company_contacts': CompanyContact,
  'company_materials': CompanyMaterial,
  'meeting_contacts': MeetingContact,
  'meeting_employee': MeetingEmployee
}

class Commands:
  @staticmethod
  def checkrole(user):
    return user.is_superuser
  
  @staticmethod
  def getalldata(args):

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(
      zip_buffer,
      'w',
      zipfile.ZIP_DEFLATED
    ) as archive:

      for filename, model in MODELS.items():
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)

        fields = [field.attname for field in model._meta.fields]

        writer.writerow(fields)
        for obj in model.objects.all().iterator(chunk_size=2000):
          try:
            row = [getattr(obj, field) for field in fields]
            writer.writerow(row)
          except:
            print(f'Пропущена запись {model.__name__} id - {obj.pk}')

        archive.writestr(
          f'{filename}.csv',
          csv_buffer.getvalue().encode('utf-8-sig')
        )
        csv_buffer.close()
      
    zip_buffer.seek(0)

    archive_name = (
      f'ContactsApp_Export_'
      f'{datetime.now():%Y%m%d_%H%M%S}.zip'
    )

    return FileResponse(
      zip_buffer,
      as_attachment=True,
      filename=archive_name
    )

  @staticmethod
  def getModels(args):
    res = ''
    for name, model in MODELS.items():
      temp_res = f'Model: {model.__name__} ({model._meta.db_table})\nFields: '
      temp_res = temp_res + '\n\t'.join([f'{field.name} ({model._meta.get_field(field.name).name})' for field in model._meta.fields]) 
      res = res + f'{temp_res}\n\n'
    return res

  @staticmethod
  def sqlQuery(args):
    if args[0].lower() != 'select':
      return 'only SELECT!!!'
    
    query = ' '.join(args)
    result = ''

    try:
      with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        temp_row = [' - '.join(map(str, row)) for row in rows]
        result = '\n'.join(temp_row) 
    except Exception as e:
      result = f'Error - {e}'  


    return query + '\n\n' +  result

  @staticmethod
  def checkConnections(args):
    model_name = args[0]
    fields = args[1:]
    mistakes = []
    for name, model in MODELS.items():
      if model.__name__ != model_name:
        continue
      data = model.objects.all()
      for item in data:
        try:
          [getattr(item, field) for field in fields]
        except Exception as e:
          mistakes.append(f'id: {getattr(item, 'id')} - {e}')
    if len(mistakes) > 0:
      return f'Errors in Model: {model_name}\n' + '\n\t'.join(mistakes)
    return 'no mistakes'

  @staticmethod
  def HelpCommand(args):
    cmds_list = [
      'all_users - show all users',
      'create_user <username> <password> [admin] - create new user',
      'reset_password <username> <password> - set new password',
      'delete_user <username> - delete user',
      'load_csv - download archive with db data',
      'models - get models structure',
      'check_con - check error connections',
      'sql <select ...> - raw sql query (only select)',
      'clear - clear output area'
    ]
    return 'Commands List\n' + '\n'.join(cmds_list)
  
  @staticmethod
  def createUser(args):
    username = args[0]
    password = args[1]
    is_admin = len(args) > 2 and args[2].lower() == "admin"

    if User.objects.filter(username=username).exists():
      return f'User exists'
    
    if is_admin:
      User.objects.create_superuser(
        username=username,
        password=password
      )
    else:
      User.objects.create_user(
        username=username,
        password=password
      )
    return f'User created'


  
  @staticmethod
  def deleteUser(args):
    username = args[0]

    user = User.objects.filter(username=username).first()

    if not user:
      return 'User Not Found'

    if user.is_superuser:
      return 'nope'
    
    user.delete()
    return 'deleted'

  @staticmethod
  def resetPassword(args):
    username = args[0]
    new_password = args[1]

    user = User.objects.get(username=username)

    if user.is_superuser:
      return 'nope'
    
    user.set_password(new_password)
    user.save()
    return 'success'
  
  @staticmethod
  def getUsers(args):
    users = User.objects.all()
    users_data = []
    for user in users:
      role = 'admin' if user.is_superuser else 'user'
      users_data.append(
        f'{user.username} ({role})'
      )
    return '\n'.join(users_data)