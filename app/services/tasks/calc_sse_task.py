import asyncio
from dataclasses import dataclass
import json
from datetime import datetime, timedelta
from typing import Callable, Tuple
from app.services.task_manager import Task
from app.services.sse_manager import manager as sse_manager
from app.calc import get_calc_functions
from app.database import data as db_data
from app.database import calc as db_calc
from app.database import holding as db_holding, customized as db_customized

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
  
  return (start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'))

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

  async def _send_data(self, data: dict | None = None, code: int = 0, message: str | None = None):
    """Sends data to the user via SSE."""
    await sse_manager.send_data(self.uid, self.TYPE, data, code, message)

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
      ret.extend([StockItem(type=r.type, code=r.code) for r in results])
    elif list_type == 3: # all
      results = db_data.get_item_infos()
      ret.extend([StockItem(type=r.type, code=r.code, name=r.name) for r in results])
    return ret

  async def _process_stock(self, stock_item: StockItem, start_date: str, end_date: str, 
                           calc_func: Callable, report_func: Callable, 
                           calc_options: dict, report_period: int):
    """Processes a single stock: fetches data, calculates, reports, and sends SSE."""
    # 1. Fetch history data
    history_df = db_data.download_history_data(stock_item.type, stock_item.code, start=start_date, end=end_date)
    if history_df is None or history_df.empty:
      return

    # 2. Perform calculation
    result_df = calc_func(history_df, calc_options)

    # 3. Generate report
    report_lines = report_func(history_df, result_df, idx=report_period, options=calc_options)

    # 4. Send report via SSE
    if report_lines:
      sse_message = {
          "cid": self.cid,
          "stock_code": stock_item.code,
          "report": report_lines
      }
      await self._send_data(data=sse_message)

  async def run(self, exit_event: asyncio.Event):
    """The main logic for orchestrating the calculation and SSE sending task."""
    try:
      # 1. Fetch main calculation item
      item = db_calc.select_algorithm_item(self.uid, self.cid)
      if not item:
        await self._send_data(code=-1, message=f"[Calc Task {self.cid}] Algorithm item not found.")  
        return
      
      # 2. Get Algorithm arguments
      args_list = db_calc.select_algorithm_item_arguments(self.cid)
      if not args_list or len(args_list) == 0:
        await self._send_data(code=-1, message=f"[Calc Task {self.cid}] No arguments found for algorithm item.")  
        return
      
      funcs: list[Tuple[Callable, Callable]] = [get_calc_functions(item.category, item.type) for item in args_list]
      func_args: list[dict] = [json.loads(arg.arguments) for arg in args_list]
      if not funcs or len(funcs) == 0:
        await self._send_data(code=-1, message=f"[Calc Task {self.cid}] No calc/report functions found for arguments.")  
        return
      
      # 3. Get Stock list
      stock_list = self._get_stock_list(item.list_type)
      if not stock_list or len(stock_list) == 0:
        await self._send_data(code=-1, message=f"[Calc Task {self.cid}] No stocks found for the specified list type.")  
        return
      
      # 4. Prepare date range
      start_date, end_date = _get_date_range(item.data_period)

      # 6. Loop through each calculation step
      for item in stock_list:
        if exit_event.is_set():
          print(f"[Calc Task {self.cid}] Task cancelled.")
          break

        history_df = db_data.download_history_data(item.type, item.code, start=start_date, end=end_date)
        if history_df is None or history_df.empty:
          print(f"[Calc Task {self.cid}] No history data for {item.code}, skipping.")
          await self._send_data(code=-1, message=f"[Calc Task {self.cid}] No history data for {item.code}, skipping.")
          continue
        
        for (calc_func, report_func), calc_options in zip(funcs, func_args):
          calc_result = calc_func(history_df, calc_options)
          calc_report = report_func(history_df, calc_result, idx=item.report_period, options=calc_options)
          if calc_report:
            sse_message = {
                "cid": self.cid,
                "stock_code": item.code,
                "report": calc_report
            }
            await self._send_data(data=sse_message)
          await asyncio.sleep(0.1)
        await asyncio.sleep(0.1)

    except asyncio.CancelledError:
      print(f"Task '{self.name}' was stopped (cancelled)." )
      await self._send_data(code=-1, message=f"[Calc Task {self.cid}] Task was cancelled.")
    except Exception as e:
      print(f"[Calc Task {self.cid}] Error: {e}")
      await self._send_data(code=-1, message=f"[Calc Task {self.cid}] Error: {e}")
    finally:
      print(f"[Calc Task {self.cid}] Finished.")
      await self._send_data(message=f"[Calc Task {self.cid}] Finished.")

      