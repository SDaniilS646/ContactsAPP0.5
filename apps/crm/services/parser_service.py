from backend.web_parser.config import SEARCH_PROVIDER, LOADER, EXTRACTOR
from urllib.parse import urlparse
import json

class WebParser:
  def web_parser(input):
    while True:
      print()

      material = input #input('What material?')

      if material.lower() == 'exit':
        break

      suppliers = SEARCH_PROVIDER.search(material)

      with open(
        'backend/web_parser/excluded_domains.json',
        encoding='utf-8'
      ) as f:
        
        excluded_domains = json.load(f)



      if not suppliers:
        return 'NOT FOUND'

      result = []

      for supplier in suppliers:
        domain = urlparse(supplier.url).netloc.lower()
        if any(excluded in domain for excluded in excluded_domains):
          continue
        pg_loaded = LOADER.load(supplier.url)
        if pg_loaded:
          # print(supplier.url)
          mails = EXTRACTOR.extract(supplier.url, pg_loaded).email
          mails = list(set(mails))
          if len(mails) == 0:
            continue
          result.append({
            'url': urlparse(supplier.url).netloc,
            'mail': mails
          })

      return result