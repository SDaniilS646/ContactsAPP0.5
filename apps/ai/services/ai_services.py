from apps.ai.models.models import AiTask, AiTaskVersion, AiQueryLog

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
      'stream':True
    }

    if response_format:
      kwargs['response_format'] = response_format

    print('Qwen в работе: ', end='', flush=True)
    t_start = time.perf_counter()
    t_first = None
    token_count = 0
    full_response = []


    stream = cls._get_client().chat.completions.create(**kwargs)
    print(time.perf_counter()- t_start)

    print('CHUNKS')

    for chunk in stream:
      if not chunk.choices:
        continue

      # reasoning = getattr(delta, 'reasoning_content', None)

      # if reasoning:
      #   if t_first is None:
      #     t_first = time.perf_counter()
      #     print(f'[TTFT: {t_first - t_start:2f}c] ', end='', flush=True)
      #   print(f'\033[90m{reasoning}\033[0m', end='', flush=True)

      text = chunk.choices[0].delta.content
      # if text:
      #   if t_first is None:
      #     t_first = time.perf_counter()
      #     print(f'[TTFT: {t_first - t_start:.2f}c] ', end='', flush=True)
      #   token_count += 1
      if text:
        full_response.append(text)
        print('.', end='', flush=True)

    elapsed = time.perf_counter()- t_start
    rate = token_count / elapsed if elapsed > 0 else 0

    print(f'\n[Готово: {token_count} ток. за {elapsed:.2f}c, {rate:.1f} ток/c]', flush=True)
    print()
    print(full_response)
    print(type(full_response))
    print(''.join(full_response))
    print(type(''.join(full_response)))
    print()
    


    # AiService.save_query_log(request=user_query, response=''.join(full_response), latency=latency, task_version=model, token_count=token_count)
    return ''.join(full_response)

  @classmethod
  def execute_ai_query_stream(cls, user_query=None, system_query=None, response_format=None, model=None, verbose=True):
    pass

class AiService:
  @staticmethod
  def save_query_log(request=None, response=None, latency=None, task_version=None, token_count=None):
    print(f'request: {request}')
    print(f'response: {response}')
    print(f'token_count: {token_count}')
    print(f'model:{task_version}')
    print(f'latency: {latency}')
    # AiQueryLog.objects.create(
    #   request_text=request,
    #   raw_response=response,
    #   latency_ms=latency,
    #   token_count=token_count,
    #   task_version=task_version
    # )
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
      if field.name in ['system_prompt', 'notes']:
        if field.name == 'notes' and task_version.values(field.name)[0][field.name] == '':
          continue
        fields_data.append({
          'field_name': field.name,
          'field_value': task_version.values(field.name)[0][field.name],
          'html_start': '<textarea disabled>',
          'html_end': '</textarea>'
        })
        continue
      fields_data.append({
        'field_name': field.name,
        'field_value': task_version.values(field.name)[0][field.name],
        'html_start': '<span>',
        'html_end': '</span>'
      })

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