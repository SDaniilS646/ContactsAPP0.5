from backend.web_parser.models import Supplier
from .search_engine import SearchEngine

class LocalSearch(SearchEngine):
  def search(self, material):
    database = {
      'Пенебанд С': [
        Supplier(
          material='Пенебанд С',
          company='Пенетрон',
          website='https://penetron.ru',
          email='info@penetron.ru',
          phone='8-800-200-70-92'
        ),
        Supplier(
          material='Пенетрон С',
          company='ПСК',
          website='https://psk-holding.ru',
          email='info@psk-holding.ru',
          phone='+7 (495) 225 22 37'
        )
      ],
      'Пенепокси 2К':[
        Supplier(
          material='Пенепокси 2К',
          company='Пенетрон',
          website='https://penetron.ru',
          email='info@penetron.ru',
          phone='8-800-200-70-92'
        )
      ]
    }

    return database.get(material, [])