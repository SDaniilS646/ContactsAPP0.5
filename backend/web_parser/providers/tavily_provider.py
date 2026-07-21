from .provider import SearchProvider

class TavilyProvider(SearchProvider):
  def search(self, material):
    urls = []
    return urls