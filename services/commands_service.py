from django.contrib.auth.models import User
from django.apps import apps

from pathlib import Path

import csv

class Commands:

  @staticmethod
  def checkrole(user):
    return user.is_superuser
  
  @staticmethod
  def getalldata(args):
    models = apps.get_models()
    return 'nice'

    for model in models:
      print(model.__name__)
      if model._meta.app_label != 'ContactsApp':
        continue
      filepath = Path('') / f'{model.__name__}.csv'
      fields = [field.name for field in model._meta.fields]
      with open(filepath, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(fields)

        for obj in model.objects.all():
          row = [getattr(obj, field) for field in fields]

          writer.writerow(row)

    return 'nice'

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