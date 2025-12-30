"""
Index Baostock
"""
from typing import Optional, List
from pandas import DataFrame
import pandas as pd
import baostock as bs
from app.logger import logger


def download_minute_data(codes: List[str], start: str, end: str, period: str = '5', adjust: str = 'qfq') -> List[Optional[DataFrame]]:
  """
  Download index minute data using Baostock
  :param codes: List of Index codes, e.g. ['sh.000001']
  :param start: Start date, e.g. '2023-01-01'
  :param end: End date, e.g. '2023-01-31'
  :param period: '5', '15', '30', '60'
  :param adjust: '3' (no adjust)
  :return: List of DataFrame or None
  """
  try:
    lg = bs.login()
    if lg.error_code != '0':
      logger.warning(f"Baostock login failed: {lg.error_msg}")
      return []

    # Map adjust
    adjust_map = {
      'qfq': '2',
      '2': '2',
      'hfq': '1',
      '1': '1',
      '': '3',
      '3': '3',
      'none': '3',
      None: '3'
    }
    adjust_flag = adjust_map.get(str(adjust).lower(), '3')

    # Clean period parameter
    frequency = str(period).lower().replace('min', '')

    # Set fields
    fields = "date,time,code,open,high,low,close,volume,amount,adjustflag"
    
    results = []
    
    for code in codes:
      rs = bs.query_history_k_data_plus(
        code=code,
        fields=fields,
        start_date=start,
        end_date=end,
        frequency=frequency,
        adjustflag=adjust_flag
      )
      
      if rs.error_code != '0':
        logger.warning(f"Baostock query failed for {code}: {rs.error_msg}")
        results.append(None)
        continue
        
      data_list = []
      while (rs.error_code == '0') and rs.next():
        data_list.append(rs.get_row_data())
        
      if not data_list:
        results.append(None)
        continue
        
      df = pd.DataFrame(data_list, columns=fields.split(","))

      # Convert numeric columns
      numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'amount']
      df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
      
      results.append(df)
      
    bs.logout()
    return results

  except Exception as e:
    logger.warning(f"Error downloading minute data: {e}")
    try:
      bs.logout()
    except:
      pass
  
  return []
