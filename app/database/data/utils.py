from datetime import datetime


def convert_history_date_1(date: str) -> str:
  return f"{date[:4]}-{date[4:6]}-{date[6:]}"

def convert_history_date_2(date: str) -> str:
  return f"{date[:4]}{date[5:7]}{date[8:]}"

def is_wordday(date: datetime = datetime.today()) -> bool:
  return date.weekday() <= 4