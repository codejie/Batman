from datetime import datetime, timedelta

def convert_history_date_1(date: str) -> str:
  return f"{date[:4]}-{date[4:6]}-{date[6:]}"

def convert_history_date_2(date: str) -> str:
  return f"{date[:4]}{date[5:7]}{date[8:]}"

def is_workday(date: datetime = datetime.today()) -> bool:
  return date.weekday() <= 4

def get_latest_workday() -> datetime:
  date = datetime.today()
  while date.weekday() > 4:
    date = date - timedelta(days=1)
  return date
  
def date_to_string_1(date: datetime) -> str:
  return date.strftime("%Y-%m-%d")

def date_to_string_2(date: datetime) -> str:
  return date.strftime("%Y%m%d")