import asyncio
import pandas as pd
import numpy as np
from dataclasses import asdict, dataclass
import json
from datetime import datetime, timedelta
from typing import Callable, Tuple
from app.services.task_manager import Task
from app.services.sse_manager import manager as sse_manager
from app.calc import list_to_df, get_calc_functions
from app.database import data as db_data
from app.database import calc as db_calc
from app.database import holding as db_holding, customized as db_customized
from app.logger import logger

def _get_date_range(period: int) -> Tuple[str, str]:
  """Converts a period code to start and end date strings."""
  end_date = datetime.now()
  if period == 0: # 3 months
    start_date = end_date - timedelta(days=90)
  elif period == 1: # 6 months
    start_date = end_date - timedelta(days=180)
  elif period == 2: # 1 year
    start_date = end_date - timedelta(days=365)
  elif period == 3: # 2 years
    start_date = end_date - timedelta(days=730)
  else:
    start_date = end_date - timedelta(days=180) # Default to 6 months
  
  return (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

def _get_report_index(report_period):
    if report_period == 0: # all
      return -1
    elif report_period == 1:
      return -3
    elif report_period == 2:
      return -7
    elif report_period == 3:
      return -30
    else:
      return 0
    
@dataclass
class StockItem:
  type: int  # 2: stock, 1: index
  code: str
  name: str | None = None

class CalcSseTask(Task):
  NAME = "calc_sse_task"
  TYPE = "calc_report"

  def __init__(self, name=None, **kwargs):
    super().__init__(name, **kwargs)
    self.uid = kwargs.get('uid')
    self.cid = kwargs.get('cid')
    if self.uid is None or self.cid is None:
      raise ValueError("uid and cid must be provided for CalcSseTask")

  async def _send_report(self, category: int, type: int, stock: StockItem, result: dict, arguments: dict):
    """Sends data to the user via SSE."""
    await sse_manager.send_data(self.uid, self.TYPE, data={
      "category": category,
      "type": type,
      "stock": asdict(stock),
      "result": result,
      "arguments": arguments
    })

  async def _send_action(self, action: str, message: str | None = None):
    """Sends a custom event to the user via SSE."""
    await sse_manager.send_event(self.uid, self.TYPE, event="action", data={"action": action, "message": message})

  def _get_stock_list(self, list_type: int) -> list[StockItem]:
    ret = []
    if list_type == 4: # holding & watchlist
      results = db_holding.records(self.uid)
      ret.extend([StockItem(type=r.type, code=r.code, name=r.name) for r in results])
      results = db_customized.records(self.uid)
      ret.extend([StockItem(type=r.type, code=r.code, name=r.name) for r in results])
    elif list_type == 0: # holding only
      results = db_holding.records(self.uid)
      ret.extend([StockItem(type=r.type, code=r.code, name=r.name) for r in results])
    elif list_type == 1: # customized only / watchlist
      results = db_customized.records(self.uid)
      ret.extend([StockItem(type=r.type, code=r.code, name=r.name) for r in results])
    elif list_type == 2: # custom only
      results = db_calc.select_algorithm_item_stock_list(self.cid)
      ret.extend([StockItem(type=r.type, code=r.code, name=r.name) for r in results])
    elif list_type == 3: # all
      results = db_data.get_item_infos()
      ret.extend([StockItem(type=r.type, code=r.code, name=r.name) for r in results])
    return ret

  async def run(self, exit_event: asyncio.Event):
    await asyncio.sleep(1)  # Short delay to ensure setup is complete
    await self._send_action(action="start")
    """The main logic for orchestrating the calculation and SSE sending task."""
    try:
      # 1. Fetch main calculation item
      item = db_calc.select_algorithm_item(self.uid, self.cid)
      if not item:
        await self._send_action(action="log", message=f"[CalcTask {self.cid}] Algorithm item not found.")  
        return
      
      # 2. Get Algorithm arguments
      args_list = db_calc.select_algorithm_item_arguments(self.cid)
      if not args_list or len(args_list) == 0:
        await self._send_action(action="log", message=f"[CalcTask {self.cid}] No arguments found for algorithm item.")  
        return
      
      funcs: list[Tuple[Callable, Callable]] = [get_calc_functions(item.category, item.type) for item in args_list]
      func_args: list[dict] = [json.loads(arg.arguments) for arg in args_list]
      if not funcs or len(funcs) == 0:
        await self._send_action(action="log",  message=f"[CalcTask {self.cid}] No calc/report functions found for arguments.")  
        return
      
      # 3. Get Stock list
      stock_list = self._get_stock_list(item.list_type)
      if not stock_list or len(stock_list) == 0:
        await self._send_action(action="log", message=f"[CalcTask {self.cid}] No stocks found for the specified list type.")  
        return
      
      # 4. Prepare date range
      start_date, end_date = _get_date_range(item.data_period)
      report_index = _get_report_index(item.report_period)

      # 6. Loop through each calculation step
      for stock in stock_list:
        if exit_event.is_set():
          logger.info(f"[CalcTask {self.cid}] Task cancelled.")
          break

        history_data = db_data.get_history_data(stock.type, stock.code, start=start_date, end=end_date)
        history_data = list_to_df(history_data)
        if history_data is None and history_data.empty:
          logger.warning(f"[CalcTask {self.cid}] No history data for {stock.code}, skipping.")
          await self._send_action(action="log",  message=f"[CalcTask {self.cid}] No history data for {stock.code}, skipping.")
          continue
        
        for arg_item in args_list:
          calc_func, report_func = get_calc_functions(arg_item.category, arg_item.type)
          if not calc_func or not report_func:
            await self._send_action(action="log",  message=f"[CalcTask {self.cid}] No calc/report functions found for {arg_item.category}/{arg_item.type}.")  
            continue

          calc_options = json.loads(arg_item.arguments)
          calc_result = calc_func(history_data, calc_options)
          calc_report = report_func(history_data, calc_result, idx=report_index, options=calc_options)
          # if calc_report:
          await self._send_report(category=arg_item.category, type=arg_item.type, stock=stock, result={
              "calc": calc_result.replace({pd.NA: None, np.nan: None}).reset_index().to_dict(orient='list') if calc_result is not None and item.show_opt == 1 else None,
              "report": calc_report
            }, arguments=calc_options)
          # else:
          #   await self._send_action(action="log",  message=f"[CalcTask {self.cid}] No report generated for {stock.code} with options {calc_options}.")
          await asyncio.sleep(0.1)
        await asyncio.sleep(0.1)

    except asyncio.CancelledError:
      logger.info(f"Task '{self.name}' was stopped (cancelled)." )
      await self._send_action(action="log", message=f"[CalcTask {self.cid}] Task was cancelled.")
    except Exception as e:
      logger.error(f"[CalcTask {self.cid}] Error: {e}")
      await self._send_action(action="log", message=f"[CalcTask {self.cid}] Error: {e}")
    finally:
      logger.info(f"[CalcTask {self.cid}] Finished.")
      await self._send_action(action="finish")
