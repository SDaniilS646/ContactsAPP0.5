from openai import OpenAI
import json
import os


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
  def execute_ai_query(cls, user_query=None, system_query=None, response_format=None, model=None):
    messages = []

    if system_query:
      messages.append({"role": "system", "content": system_query})

    messages.append({"role": "user", "content": user_query})

    kwargs = {
      'model':model or os.getenv('LLM_MODEL_NAME'),
      'messages':messages,
      'temperature':float(os.getenv('LLM_TEMPERATURE', 0))
    }

    if response_format:
      kwargs['response_format'] = response_format

    # try:
    response = cls._get_client().chat.completions.create(**kwargs)
    return response.choices[0].message.content
    # except:
    #   return 'AI response error'
