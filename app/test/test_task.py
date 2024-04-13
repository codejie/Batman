import unittest
import os
from app.task_manager import Task, TaskType, taskManager

def func(**kwargs):
    pass

class TestTask(unittest.TestCase):
    def test_save(self):
        print(f'==========={os.getcwd()}')
        task: Task  = Task(
            type=TaskType.FinderStrategyInstance,
            id='123456789',
            trigger={
                'mode': 'daily',
                'days': '0-4',
                'hour': 22,
                'minute': 1
            },
            func=func,
            attach={
                'title': 'ttt',
                'args': {
                    'id': '123456789',
                    'a': 1
                }
            }
        )

        id = taskManager.save_task(task)

        self.assertEqual(id, '123456789')

    def test_loads(self):
        taskManager.load_tasks()

        self.assertTrue(True)

    def test_delete(self):
        taskManager.delete_task('123456789')
        self.assertTrue(True)