from apps.ai.models.models import AiTask, AiTaskVersion, AiQueryLog, AiExample
from apps.crm.services.model_services.material_service import MaterialService

from openai import OpenAI
import json
import os

import time


class AiExecutionService:
  _client = None
  @classmethod
  def _get_client(cls):
    if cls._client is None:
      cls._client = OpenAI(
        base_url=os.getenv('LLM_BASE_URL'),
        api_key=os.getenv('LLM_API_KEY')
      )
    return cls._client
  
  @classmethod
  def execute_ai_query(cls, user_query=None, system_query=None, response_format=None, model=None, temperature=0):
    messages = []
    if not model:
      print('NO MODEL')
      return []

    if system_query:
      messages.append({"role": "system", "content": system_query})

    messages.append({"role": "user", "content": user_query})

    kwargs = {
      'model':model.model_name,
      'messages':messages,
      'temperature':temperature,
      'stream':True,
      'stream_options': {"include_usage": True}
    }

    if response_format:
      kwargs['response_format'] = response_format

    print('Qwen в работе: ', end='', flush=True)
    t_start = time.perf_counter()
    t_first = None
    token_count = None
    full_response = []


    stream = cls._get_client().chat.completions.create(**kwargs)
    print(time.perf_counter()- t_start)

    for chunk in stream:
      if not chunk.choices:
        if hasattr(chunk, 'usage') and chunk.usage:
          prompt_tokens = chunk.usage.prompt_tokens or 0
          print(f'prompt tokens - {prompt_tokens}')
          token_count = chunk.usage.completion_tokens or 0
        continue

      text = chunk.choices[0].delta.content
      if text:
        full_response.append(text)
        print('.', end='', flush=True)

    latency = time.perf_counter()- t_start

    if token_count is None:
      token_count = 0
    return ''.join(full_response), latency, token_count, prompt_tokens

  @classmethod
  def execute_ai_query_stream(cls, user_query=None, system_query=None, response_format=None, model=None, verbose=True):
    pass

class AiService:
  @staticmethod
  def prepare_dpo_dataset():
    dataset = []
    requests = AiExample.objects.filter(is_active=True).values
    for req in requests:
      print(f'{req.request_text} - {req.materials.name} - {req.example_check}')

  @staticmethod
  def save_material_label(labeled_data):
    CHECKS = {
      'true': True,
      'false': False,
      '': None
    }
    examples = AiExample.objects.all()
    prev_data = []
    new_data = []
    for idx, example in enumerate(examples):
      prev_data.append(
        {
          'id':examples[idx].id,
          'check':examples[idx].example_check,
          'is_active':examples[idx].is_active
        }
      )
      new_data.append(
        {
          'id':labeled_data[idx]['id'],
          'check':CHECKS.get(labeled_data[idx]['value']),
          'is_active':labeled_data[idx]['is_active']
        }
      )

    for item in new_data:
      if item not in prev_data:
        AiExample.objects.filter(id=item['id']).update(
          example_check=item['check'],
          is_active=item['is_active']
        )

  @staticmethod
  def save_query_log(request=None, response=None, latency=None, task_version=None, token_count=None, prompt_tokens=None):
    id = AiQueryLog.objects.create(
      request_text=request,
      raw_response=response,
      latency_ms=latency,
      token_count=token_count,
      task_version=task_version,
      prompt_tokens=prompt_tokens
    ).id
    return id

  @staticmethod
  def save_ai_example(source=None, request_text=None, material_id=None, request_id=None):
    if len(AiExample.objects.filter(request_text=request_text, materials=MaterialService.get_material(material_id))) > 0:
      return
    AiExample.objects.create(
      request=AiQueryLog.objects.filter(id=request_id).first(),
      request_text=request_text,
      materials=MaterialService.get_material(material_id),
      example_check=None,
      source=source
    )
    return
  
  @staticmethod
  def get_ai_models():
    tasks = AiTask.objects.all()
    output_list = [{'tech_name':task.name, 'description':task.description, 'id':task.id} for task in tasks]

    return output_list

  @staticmethod
  def get_ai_model(id):
    task = AiTask.objects.filter(id=id).first()
    return task

  @staticmethod
  def get_ai_versions(task):
    versions = AiTaskVersion.objects.filter(task=task)

    return versions

  @staticmethod
  def get_last_version(task):
    last_version = AiService.get_ai_versions(task).order_by('-version').first()
    return last_version

  @staticmethod
  def activate(version_id):
    version = AiTaskVersion.objects.filter(id=version_id)
    AiTaskVersion.objects.filter(task=version.first().task).update(is_active=False)
    version.update(is_active=True)

    return

  @staticmethod
  def get_version_info(version_id):
    fields = AiTaskVersion._meta.get_fields()
    task_version = AiTaskVersion.objects.filter(id=version_id)
    fields_data = []
    for field in fields:
      if field.name in ['created_at', 'updated_at', 'created_by', 'updated_by', 'task', 'id']:
        continue
      if field.name == 'notes' and task_version.values(field.name)[0][field.name] == '':
        continue

      fields_data.append({
        'field_name': field.name,
        'field_value': task_version.values(field.name)[0][field.name],
      })
      
    
    for item in fields_data:
      print(item)

    return fields_data

  @staticmethod
  def create_version(input_data):
    task = AiService.get_ai_model(input_data['task_id'])
    new_version_id = AiService.get_last_version(task).version + 1
    id = AiTaskVersion.objects.create(
      task=task,
      version=new_version_id,
      system_prompt=input_data['system_prompt'] if input_data['system_prompt'] else '',
      model_name=input_data['model_name'],
      max_tokens=input_data['max_tokens'] if input_data['max_tokens'] else 2048,
      temperature=input_data['temperature'] if input_data['temperature'] else 0,
      notes=input_data['notes'] if input_data['notes'] else ''
    ).id
    AiService.activate(id)
    return