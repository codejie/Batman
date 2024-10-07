"""
System Configuration
"""

"""
System Task Triggers
"""
UPDATE_DAILY_TRIGGER = {
  'mode': 'daily',
  'days': '0-6',
  'hour': 11,
  'minute': 3
}

UPDATE_DAILY_THIRD_TRIGGER = {
  'mode': 'daily',
  'days': '0-6',
  'hour': 11,
  'minute': 0
}

"""
Third Stock Data Origin
"""
THIRD_STOCK_DATA_FROM_DATABASE = True # data from local data, otherwise internet