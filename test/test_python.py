
import unittest
import pandas as pd

class TestPython(unittest.TestCase):
    def test_dataframe(self):
        df = pd.DataFrame({
            'a': [1, 2],
            'b': [3, 4]
        })
        print(df)
        print(df.to_dict('list'))


        # l = list()
        l = { 'a': [1,2]}
        print(l)
        print(type(l))

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()