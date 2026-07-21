import re
from bs4 import BeautifulSoup

from backend.web_parser.models import Supplier

from .extractor import ContactExtractor

class RegexExtractor(ContactExtractor):
  def extract(self, url, html):
    soup = BeautifulSoup(html, 'lxml')
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    emails = email_pattern.findall(html)
    print(emails)
    # emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', html)

    phones = re.findall(r'\+?\d[\d\s\-\(\)]{8,}', html)

    return Supplier(
      company='',
      website=url,
      email=emails,
      phone=''
    )