from app.services.client_manager import WSClientManager
from app.services.scheduler import ServiceScheduler
from app.services.spot_data_fetch import SpotDataClientManager, SpotDataFetchService
from app.setting import SERVICE_SCHEDULER_ENABLED, SERVICE_SPOT_DATA_ENABLED

serviceScheduler = ServiceScheduler()
# serviceScheduler.register_service(type=Service, name="test_service")
if SERVICE_SPOT_DATA_ENABLED:
  serviceScheduler.register_service(type=SpotDataFetchService, name=SpotDataFetchService.NAME)

wsClientManager: dict[str, WSClientManager] = {}
if SERVICE_SPOT_DATA_ENABLED:
  wsClientManager[SpotDataClientManager.NAME] = SpotDataClientManager(service=serviceScheduler.get_service(SpotDataFetchService.NAME))
