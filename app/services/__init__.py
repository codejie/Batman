from app.services.task_spot_data import SpotDataFetchTask
from app.setting import TASK_SPOT_DATA_FETCH_ENABLED
from app.services.task_manager import taskManager
from app.services.task_spot_data import spotDataClientManagerTask

# serviceScheduler = ServiceScheduler()
# # serviceScheduler.register_service(type=Service, name="test_service")
# if SERVICE_SPOT_DATA_ENABLED:
#   serviceScheduler.register_service(type=SpotDataFetchService, name=SpotDataFetchService.NAME)

# wsClientManager: dict[str, WSClientManager] = {}
# if SERVICE_SPOT_DATA_ENABLED:
#   wsClientManager[SpotDataClientManager.NAME] = SpotDataClientManager(service=serviceScheduler.get_service(SpotDataFetchService.NAME))
#   wsClientManager[SpotDataClientManager.NAME].start()

def start_tasks() -> None:
  taskManager.start()
  if TASK_SPOT_DATA_FETCH_ENABLED:
    spotTask = taskManager.add_task(task=SpotDataFetchTask)
    spotDataClientManagerTask.set_fetch_task(spotTask)
    taskManager.add_instance(spotDataClientManagerTask)


def shutdown_tasks() -> None:
  taskManager.shutdown()