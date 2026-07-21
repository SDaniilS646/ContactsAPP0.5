from backend.web_parser.providers.provider import SearchProvider
from backend.web_parser.models import SearchResult

from yandex_ai_studio_sdk import AIStudio

URL = 'https://searchapi.api.cloud.yandex.net/v2/web/search'

class YandexSearchProvider(SearchProvider):
  def __init__(
      self, api_key, folder_id
  ):
    super().__init__()
    self.sdk = AIStudio(
      folder_id=folder_id,
      auth=api_key,
    )
    
  def execute_query(self, material):
    urls = []

    # Выполнение поиска
    search = self.sdk.search_api.web(search_type="ru")

    results = search.run(material)

    for doc in results.docs:
      urls.append(
        SearchResult(
          title=doc.title,
          url=doc.url,
          snippet=''
        )
      )

    return urls