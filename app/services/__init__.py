

from app.services.scheduler import ServiceScheduler
from app.services.service import Service
from app.services.spot_data_fetch import SpotDataFetchService


serviceScheduler = ServiceScheduler()
serviceScheduler.register_service(type=Service, name="test_service")
serviceScheduler.register_service(type=SpotDataFetchService, name="spot_data_fetch_service")
