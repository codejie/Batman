
import unittest
import pandas as pd

import pickle
from app.task_manager import TaskType, Task

class TestPython(unittest.TestCase):
    def test_dataframe(self):
        df = pd.DataFrame({
            'a': [1, 2],
            'b': [3, 4]
        })
        print(df['a'].iloc[-1])
        print(df['b'].iloc[0])
        print(df)
        print(df.to_dict('list'))


        # l = list()
        l = { 'a': [1,2]}
        print(l)
        print(type(l))

        self.assertTrue(True)

    def test_kwargs(self, kwargs):
        if 'i' in kwargs:
            i = kwargs['i']
            print(i)

        j = kwargs['j']
        print(j)

    def test_call_kwargs(self):
        self.test_kwargs(kwargs={'j': 1, 'i':2})

        self.assertTrue(True)

    def test_json(self):
        task: Task  = Task(
            type=TaskType.FinderStrategyInstance,
            id='123',
            trigger={
                'mode': 'daily',
                'days': '0-4',
                'hour': 22,
                'minute': 1
            },
            element={
                'title': 'ttt',
                'args': {
                    'a': 1
                }
            }
        )

        print(task)

        a = pickle.dumps(task)

        print(a)

        b = pickle.loads(a)
        print(type(b))
        print(b)
        print(b.trigger)

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()