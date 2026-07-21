from abc import ABC, abstractmethod
from backend.web_parser.models import Supplier

class ContactExtractor(ABC):
  @abstractmethod
  def extract(self, url: str, html: str) -> Supplier:
    pass