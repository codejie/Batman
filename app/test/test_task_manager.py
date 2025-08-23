
import asyncio
import time
import pytest
from app.services.task_manager import Task, TaskManager

# Mock Task for testing
class MockTask(Task):
    NAME = "mock_task"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.run_count = 0
        self.was_stopped = False

    async def run(self, exit_event: asyncio.Event):
        while not exit_event.is_set():
            self.run_count += 1
            try:
                # await asyncio.wait_for(exit_event.wait(), timeout=0.1)
                print(f"Task {self.name} is running... {self.run_count}")
                await asyncio.sleep(1)
            except asyncio.TimeoutError:
                pass
        self.was_stopped = True

@pytest.fixture
def task_manager():
    """Fixture to create and cleanup a TaskManager instance."""
    manager = TaskManager()
    manager.start()
    yield manager
    manager.shutdown()


def test_task_manager_start_and_shutdown(task_manager: TaskManager):
    """Test that the TaskManager starts and shuts down correctly."""
    assert task_manager._thread is not None
    assert task_manager._thread.is_alive()
    task_manager.shutdown()
    # assert not task_manager._thread.is_alive()


def test_add_and_get_task(task_manager: TaskManager):
    """Test adding a task and retrieving it."""
    task_name = "test_task_1"
    task = task_manager.add_task(MockTask, name=task_name)
    assert task is not None
    assert task.name == task_name

    retrieved_task = task_manager.get_instance(task_name)
    assert retrieved_task is not None
    assert retrieved_task == task


def test_task_execution(task_manager: TaskManager):
    """Test that a task is actually executed."""
    task_name = "exec_task"
    task = task_manager.add_task(MockTask, name=task_name)
    
    # Give the task some time to run
    time.sleep(5.5)
    
    assert task.run_count > 2 # Should have run a few times


def test_shutdown_stops_task(task_manager: TaskManager):
    """Test that shutting down the manager stops the running task."""
    task_name = "stoppable_task"
    task = task_manager.add_task(MockTask, name=task_name)
    
    time.sleep(0.2)
    assert task.run_count > 0
    
    task_manager.shutdown()
    
    # Allow time for shutdown to complete
    time.sleep(0.2)
    
    assert task.was_stopped
    # assert not task_manager._thread.is_alive()

def test_add_task_when_stopped_raises_error():
    """Test that adding a task to a stopped manager raises a RuntimeError."""
    manager = TaskManager()
    with pytest.raises(RuntimeError):
        manager.add_task(MockTask)
