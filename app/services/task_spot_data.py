from app.database.data.define import SpotData
from app.services.task_manager import Task


class CustomizedSpoData:
  def __init__(self, index: str, stocks: list[SpotData] = [], indices: list[SpotData] = []):
    self.index: str = index
    self.stocks: list[SpotData] = stocks
    self.indices: list[SpotData] = indices

class SpotDataFetchService(Task):
  NAME: str = "spot_data_fetch_task"
  __PERIOD: int = 15