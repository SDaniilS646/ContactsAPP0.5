from ddgs import DDGS

from backend.web_parser.providers.provider import SearchProvider
from backend.web_parser.models import SearchResult


class DuckDuckGoProvider(SearchProvider):
  def execute_query(self, material: str):
    urls = []

    print('START PARSING -DGGS')
    with DDGS() as ddgs:
      search_results = ddgs.text(
        material,
        max_results=10,
        backend='yandex'
      )
      print('FOUND SMTH')

      for item in search_results:
        urls.append(
          SearchResult(
            title=item['title'],
            url=item['href'],
            snippet=item['body']
          )
        )
    return urls