from django.contrib.auth.models import User
from django.apps import apps
from django.http import FileResponse

from apps.companies.models import Companies
from apps.contacts.models import Contacts
from apps.materials.models import Materials
from apps.meetings.models import Meetings
from apps.employees.models import Employees
from apps.connection_models import CompanyContact, CompanyMaterial, MeetingContact, MeetingEmployee

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

        fields = [field.name for field in model._meta.fields]

        writer.writerow(fields)
        for obj in model.objects.all():
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
  def HelpCommand(args):
    cmds_list = [
      'all_users - show all users',
      'create_user <username> <password> [admin] - create new user',
      'reset_password <username> <password> - set new password',
      'delete_user <username> - delete user'
    ]
    return '\n'.join(cmds_list)
  
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