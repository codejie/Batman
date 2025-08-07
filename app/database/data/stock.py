"""
Stock
"""
from typing import Optional
from pandas import DataFrame
import akshare as ak
from sqlalchemy import delete
from app.database import dbEngine
from app.database.data import define as Define
from app.database.data import utils as Utils

from app.logger import logger

# def download_list() -> None:
#   # delete
#   stmt = delete(Define.InfoTable).where(Define.InfoTable.type == Define.TYPE_STOCK)
#   dbEngine.delete_stmt(stmt)
#   # download
#   stock_info = ak.stock_info_a_code_name()
#   stock_info['type'] = Define.TYPE_STOCK
#   stock_info['market'] = None
#   data = stock_info.to_dict(orient='records')
#   dbEngine.bulk_insert_data(Define.InfoTable, data)

def download_list() -> Optional[DataFrame]:
  # delete
  # stmt = delete(Define.InfoTable).where(Define.InfoTable.type == Define.TYPE_STOCK)
  # dbEngine.delete_stmt(stmt)
  # download
  stock_info = ak.stock_info_a_code_name()
  if not stock_info.empty:
    stock_info['type'] = Define.TYPE_STOCK
    stock_info['market'] = None

    return stock_info
  return None

def get_name(code: str) -> Optional[str]:
  return Define.get_name(Define.TYPE_STOCK, code)

def download_history_data(code: str, start: str, end: str, period: str = 'daily', adjust: str = 'qfq') -> Optional[DataFrame]:
  data = ak.stock_zh_a_hist(symbol=code, period=period, adjust=adjust, start_date=start, end_date=end)

  if not data.empty:
    data = data.drop('股票代码', axis=1)
    data.set_index('日期', inplace=True)
    return data
  else:
    return None

# def fetch_history_data(code: str, start: str, end: str, period: str = 'daily', adjust: str = 'qfq') -> list[Define.HistoryData]:
#   return Define.fetch_history_data(Define.TYPE_STOCK, code, start, end, period, adjust)

def download_spot_data(codes: list[str] = None) -> Optional[DataFrame]:
  try:
    data = ak.stock_zh_a_spot_em()
    if not data.empty:
      # data = data.drop('序号')
      # data.set_index('代码', inplace=True)
      data = data.rename(columns={
        '市盈率-动态': '市盈率',
        '5分钟涨跌': '涨跌5分钟',
        '60日涨跌幅': '涨跌幅60日'
      })
      if codes is not None:
        data = data[data['代码'].isin(codes)]
      return data
  except Exception as e:
    logger.warning(f"Error downloading spot data: {e}")
  return None

################################################
"""
Stock Info
"""
def download_info(code: str) -> Optional[DataFrame]:
  try:
    data = ak.stock_individual_info_em(symbol=code)
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading stock info for {code}: {e}")
  return None

"""
财务指标数据
"""
def download_financial_abstract_indicator(code: str, indicator: str = '按报告期') -> Optional[DataFrame]:
  """
    indicator:  choice of {"按报告期", "按年度", "按单季度"}
  """
  try:
    data = ak.stock_financial_abstract_ths(symbol=code, indicator=indicator)
    if not data.empty:
      # data = data.set_index('报告日期')
      return data
  except Exception as e:
    logger.warning(f"Error downloading financial indicator {indicator} for {code}: {e}")
  return None

"""
财务分析指标数据
"""
def download_financial_analysis_indicator(code: str, start: str = "2020") -> Optional[DataFrame]:
  try:
    data = ak.stock_financial_analysis_indicator(symbol=code, start_year=start)
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading financial analysis for {code}: {e}")
  return None

"""
现金流数据(报告期)
"""
def download_cash_report_data(code: str) -> Optional[DataFrame]:
  try:
    data = ak.stock_cash_flow_sheet_by_report_em(symbol=code)
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading cash report data for {code}: {e}")
  return None

"""
估值指标
"""
def download_valuation_indicator(code: str) -> Optional[DataFrame]:
  try:
    data = ak.stock_a_indicator_lg(symbol=code)
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading valuation indicator for {code}: {e}")
  return None

"""
业绩报表
"""
# def download_performance_report(date: str) -> Optional[DataFrame]:
#   try:
#     data = ak.stock_yjbb_em(date=date)# .stock_yjbb_em(symbol=code)
#     if not data.empty:
#       return data
#   except Exception as e:
#     logger.warning(f"Error downloading performance report for {code}: {e}")
#   return None

"""
分红配股
"""
# def download_dividend_distribution(code: str) -> Optional[DataFrame]:
#   try:
#     data = ak.stock_fhpg_em(symbol=code)
#     if not data.empty:
#       return data
#   except Exception as e:
#     logger.warning(f"Error downloading dividend distribution for {code}: {e}")
#   return None

"""
行业数据
"""
def _download_industry_data() -> Optional[DataFrame]:
  try:
    data = ak.stock_board_industry_name_em()
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading industry data : {e}")
  return None

"""
行业排名
"""
# def download_industry_rank(symbol: str = '行业排名') -> Optional[DataFrame]:
#   try:
#     data = ak.stock_rank_em(symbol=symbol)
#     if not data.empty:
#       return data
#   except Exception as e:
#     logger.warning(f"Error downloading industry rank for {symbol}: {e}")
#   return None

"""
公司新闻
"""
# def download_company_news(code: str) -> Optional[DataFrame]:
#   try:
#     data = ak.stock_news_em(symbol=code)
#     if not data.empty:
#       return data
#   except Exception as e:
#     logger.warning(f"Error downloading company news for {code}: {e}")
#   return None

"""
公司公告
"""
# def download_company_announcements(code: str) -> Optional[DataFrame]:
#   try:
#     data = ak.stock_zh_a_alerts_cls(symbol=code)
#     if not data.empty:
#       return data
#   except Exception as e:
#     logger.warning(f"Error downloading company announcements for {code}: {e}")
#   return None

"""
个股研报
"""
def download_research_report(code: str) -> Optional[DataFrame]:
  try:
    data = ak.stock_research_report_em(symbol=code)
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading research report for {code}: {e}")
  return None

