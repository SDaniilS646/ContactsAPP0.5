from dataclasses import dataclass, field

@dataclass
class SearchResult:
  title: str
  url: str
  snippet: str

@dataclass
class Supplier:
  # material: str
  company: str
  website: str
  
  phone: str

  email: list[str] = field(default_factory=list)

