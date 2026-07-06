import json
import os
from typing import Literal, Optional, cast

from app.logger import logger

DATA_SOURCE_AKSHARE = 'akshare'
DATA_SOURCE_TENCENT = 'tencent'
DATA_SOURCE_CHOICES = {DATA_SOURCE_AKSHARE, DATA_SOURCE_TENCENT}
DEFAULT_DATA_CONFIG = {
  'market_data_source': DATA_SOURCE_AKSHARE
}
DATA_CONFIG_PATH = './app/db/data_config.json'

MarketDataSource = Literal['akshare', 'tencent']

def normalize_market_data_source(source: Optional[str]) -> MarketDataSource:
  if source in DATA_SOURCE_CHOICES:
    return cast(MarketDataSource, source)
  return DATA_SOURCE_AKSHARE

def read_data_config() -> dict:
  config = DEFAULT_DATA_CONFIG.copy()
  if os.path.exists(DATA_CONFIG_PATH):
    try:
      with open(DATA_CONFIG_PATH, 'r', encoding='utf-8') as f:
        saved = json.load(f)
        if isinstance(saved, dict):
          config.update(saved)
    except Exception as e:
      logger.warning(f"Error reading data config: {e}")

  config['market_data_source'] = normalize_market_data_source(config.get('market_data_source'))
  return config

def save_data_config(market_data_source: str) -> dict:
  os.makedirs(os.path.dirname(DATA_CONFIG_PATH), exist_ok=True)
  config = {
    'market_data_source': normalize_market_data_source(market_data_source)
  }
  with open(DATA_CONFIG_PATH, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
  return config

def get_market_data_source() -> MarketDataSource:
  return read_data_config()['market_data_source']
