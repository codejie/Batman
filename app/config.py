"""
System Configuration
"""

"""
System Task Triggers
"""
UPDATE_DAILY_TRIGGER = {
  'mode': 'daily',
  'days': '0-5',
  'hour': 16,
  'minute': 28
}

UPDATE_DAILY_THIRD_TRIGGER = {
  'mode': 'daily',
  'days': '0-5',
  'hour': 22,
  'minute': 1
}

"""
Third Stock Data Origin
"""
THIRD_STOCK_DATA_FROM_DATABASE = True # data from local data, otherwise internet