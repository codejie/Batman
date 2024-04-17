import unittest
import os
from app.task_manager import Task, TaskType, taskManager
from app.task.daily_data_check import DataItem, select_last_item, insert_last_item, fetch_stock_history

from datetime import datetime, timedelta

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


    def test_select_last_item(self):
        ret = select_last_item(DataItem.STOCK_DAILY_HISTORY)
        print(ret)

        self.assertTrue(True)

    def test_insert_last_item(self):
        data = {
            DataItem.STOCK_DAILY_HISTORY
        }

        insert_last_item(
            item=DataItem.STOCK_DAILY_HISTORY,
            start=datetime.now(),
            end=datetime.now() + timedelta(days=1),
            result=0,
            arg1=1
            )

        self.assertTrue(True)

    def test_fetch_stock_history(self):
        rows = fetch_stock_history()
        print(f'insert {rows}')

        self.assertTrue(True)
        
        