from abc import ABC, abstractmethod

class PageLoader(ABC):
  @abstractmethod
  def load(self, url: str) -> str:
    pass