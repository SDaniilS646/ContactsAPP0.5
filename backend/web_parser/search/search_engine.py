from abc import ABC, abstractmethod

class SearchEngine(ABC):
  @abstractmethod
  def search(self, material: str):
    pass