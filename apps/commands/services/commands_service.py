from django.contrib.auth.models import User
from django.apps import apps
from django.http import FileResponse
from django.db import connection

from apps.crm.models.models import Company, Contact, Material, Meeting, Employee
from apps.crm.models.connections import CompanyContact, CompanyMaterial, MeetingContact, MeetingEmployee

from apps.sender.models import TrainingExample, ModelVersion
from apps.sender.sender_services import work_classifier, test_model

from apps.ai.models import AiTask, AiTaskVersion

from backend.ai.ai_service import AiService

from django.utils import timezone

from pathlib import Path

import csv
import io
import zipfile
import json
from datetime import datetime

from openai import OpenAI

MODELS = {
  'companies': Company,
  'contacts': Contact,
  'meetings': Meeting,
  'materials': Material,
  'employees': Employee,
  'company_contacts': CompanyContact,
  'company_materials': CompanyMaterial,
  'meeting_contacts': MeetingContact,
  'meeting_employee': MeetingEmployee
}

class Commands:

  @staticmethod
  def create_ai_task(args):
    model_name = args[0]
    description = args[1].split('_')
    AiTask.objects.create(
      name = model_name,
      description = description,
      created_at = timezone.now(),
      created_by=None,
      updated_at = timezone.now(),
      updated_by=None
    )

    return 'model created'

  @staticmethod
  def get_ai_models(args):
    tasks = AiTask.objects.all()

    output_list = [{'name':task.name, 'description':task.description} for task in tasks]
    output = ''
    for item in output_list:
      output = f'{output}\n{item['name']} - {item['description']}'

    return output

  @staticmethod
  def activate_ai_model_version(args):
    task = AiTask.objects.filter(name=args[0]).first()
    versions = AiTaskVersion.objects.filter(task=task)
    version_numbers = [version['version'] for version in versions.values('version')]
    version = int(args[1]) if len(args) == 2 else max(version_numbers)

    if version not in version_numbers:
      return f'У модели нет такой версии, доступны: {'; '.join(version_numbers)}'

    versions.update(is_active=False)
    versions.filter(version=version).update(is_active=True)

    return f'Model {task.name} - v{version} activated'
  

  @staticmethod
  def set_ai_task_version(args):
    task = AiTask.objects.filter(name=args[0]).first()

    prev_versions = AiTaskVersion.objects.filter(task=task)

    if len(prev_versions) == 0:
      version = 1
    else:
      versions = [version['version'] for version in prev_versions.values('version')]
      version = max(versions) + 1

    prompt=f'prompt{args[1]}'

    model_name = 'qwen2:7b-instruct'
    temperature = 0

    is_active = True


    AiTaskVersion.objects.create(
      task=task,
      version=version,
      system_prompt=prompt,
      model_name=model_name,
      lora_adapter_path='',
      temperature=temperature,
      max_tokens=2048,
      response_format=None,
      is_active=is_active,
      notes='',
      created_at = timezone.now(),
      created_by=None,
      updated_at = timezone.now(),
      updated_by=None
    )

    return 'version created'

  @staticmethod
  def ai_cmd(args):
    response = AiService.execute_ai_query(user_query=' '.join(args))
    answer = response.choices[0].message.content
    return f'AI answer: {answer}'

  @staticmethod
  def model_list(args):
    result = []
    models = ModelVersion.objects.all()
    for model in models:
      metrics = model.metrics.get('report')
      if metrics:
        metrics = metrics.get('accuracy')
      result.append(f'{model.model_type} v{model.version}: {model.Training_examples_count} examples; accuracy: {metrics}')
    return '\n'.join(result)

  @staticmethod
  def model_activate(args):
    from django.db import transaction
    model_name = args[0] if len(args) > 0 else None
    model_version = args[1] if len(args) > 1 else None
    models = ModelVersion.objects.filter(model_type = model_name).order_by('version')
    if not models:
      unique_models = list(set([model.model_type for model in ModelVersion.objects.all()]))
      return f'❌ Unknown model. Choose model from list:\n\n{"\n".join(unique_models)}'
    
    model_versions = [model.version for model in models]
    model_versions = list(set(model_versions))
    if not model_version:
      models.update(is_active=False)
      chosen_model = models.filter(version = model_versions[-1]).update(is_active=True)
      return f'⚠️ No model signed. Activated last created model: v{model_versions[-1]}'

    with transaction.atomic():
      models.update(is_active=False)
      try:
        chosen_model = models.filter(version = model_version).update(is_active=True)
        output = f'✅ Model activated. Model version: {chosen_model}'
      except:
        output = '❌ Version type error'
    
    return output
  
  @staticmethod
  def checkrole(user):
    return user.is_superuser

  @staticmethod
  def import_training_model(args):
    pending_file_path = Path(__file__).parent.parent.parent.parent / 'backend' / 'xl_sender' / 'ml_backend' / 'labeled_works.json'

    TrainingExample.objects.all().delete()

    with open(pending_file_path, 'r', encoding='utf-8') as file:
      data = json.load(file)

    for item in data:
      TrainingExample.objects.create(
        text = item.get('name'),
        label = item.get('category'),
        predicted_label = item.get('predicted category'),
        uncertainity_score = float(item['probability'].replace('%', '').strip()) / 100 if item.get('probability') else None,
        status = 'pending' if item.get('predicted category') else 'labeled'
      )
    
    return True

  @staticmethod
  def train_model(args):

    training_results = work_classifier()

    return training_results

  @staticmethod
  def test_model(args):
    testing_results = test_model(args)

    return testing_results
  
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