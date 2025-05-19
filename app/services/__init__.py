

from app.services.scheduler import ServiceScheduler
from app.services.service import Service
from app.services.spot_data_fetch import SpotDataFetchService
from app.setting import SERVICE_SPOT_DATA_ENABLED


serviceScheduler = ServiceScheduler()
# serviceScheduler.register_service(type=Service, name="test_service")
if SERVICE_SPOT_DATA_ENABLED:
  serviceScheduler.register_service(type=SpotDataFetchService, name=SpotDataFetchService.NAME)
