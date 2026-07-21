from .providers.mock_provider import MockProvider
from .providers.yandex_provider import YandexSearchProvider
from .providers.duckduckgo_provider import DuckDuckGoProvider

from .loader.request_loader import RequestsLoader

from .extractors.regex_extractor import RegexExtractor

import os
from dotenv import load_dotenv

load_dotenv()
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEXFOLDER_ID = os.getenv("FOLDER_ID")

SEARCH_PROVIDER = DuckDuckGoProvider() 
# SEARCH_PROVIDER = YandexSearchProvider(YANDEX_API_KEY, YANDEXFOLDER_ID) 

LOADER = RequestsLoader()

EXTRACTOR = RegexExtractor()


