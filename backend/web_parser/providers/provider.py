from abc import ABC, abstractmethod

from backend.web_parser.models import SearchResult
from .query_builder import QueryBuilder


class SearchProvider(ABC):
  def __init__(self):
    self.query_builder = QueryBuilder()
  
  def search(self, material: str):
    queries = self.query_builder.build_query(material)

    results = []

    for query in queries:
      # try:
      temp = self.execute_query(query)
      results.extend(temp)
      # except:
      #   continue
      
    return self.remove_duplicates(results)

  def remove_duplicates(self, results):
    unique = {}
    for item in results:
      unique[item.url] = item
    
    return list(unique.values())

  @abstractmethod
  def execute_query(self, material: str) -> list[SearchResult]:
    pass