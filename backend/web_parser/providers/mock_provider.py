from backend.web_parser.models import Supplier
from .provider import SearchProvider

class MockProvider(SearchProvider):
  def search(self, material):
    urls = []
    return urls