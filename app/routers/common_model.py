from datetime import datetime, date
from app.routers.definition import BaseModel

class DataFrameSetModel(BaseModel):
  columns: list[str]
  data: list[list[str | int | float | datetime | date | None ]]
