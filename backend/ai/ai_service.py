from openai import OpenAI
import json
import os

import time


class AiService:
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
      'model':model,
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

    for chunk in stream:
      if not chunk.choices:
        continue
      delta = chunk.choices[0].delta

      reasoning = getattr(delta, 'reasoning_content', None)

      if reasoning:
        if t_first in None:
          t_first = time.perf_counter()
          print(f'[TTFT: {t_first - t_start:2f}c] ', end='', flush=True)
        print(f'\033[90m{reasoning}\033[0m', end='', flush=True)

      text = delta.content
      if text:
        if t_first is None:
          t_first = time.perf_counter()
          print(f'[TTFT: {t_first - t_start:.2f}c] ', end='', flush=True)
        token_count += 1
        full_response.append(text)
        print(text, end='', flush=True)

    elapsed = time.perf_counter()- t_start
    rate = token_count / elapsed if elapsed > 0 else 0
    print(f'\n[Гтово: {token_count} ток. за {elapsed:.2f}c, {rate:.1f} ток/c]', flush=True)

    
    return ''.join(full_response)

  @classmethod
  def execute_ai_query_stream(cls, user_query=None, system_query=None, response_format=None, model=None, verbose=True):
    pass
