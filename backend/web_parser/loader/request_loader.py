
import requests
from .page_loader import PageLoader

class RequestsLoader(PageLoader):
  def load(self, url):
    try:
      response = requests.get(
        url,
        timeout=15,
        headers={
          'User-Agent': 'Mozilla/5.0'
        }
      )
      return response.text
    except:
      print('Ошибка')
      return None
    