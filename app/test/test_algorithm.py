import unittest

from app.strategy.algorithm.m_up_n_down import MUpNDownAlgorithem

class Test_Algorithm(unittest.TestCase):
    def test_m_up_n_down(self):
        algorithm = MUpNDownAlgorithem()
        algorithm.run()
        print('==================end')
        self.assertTrue(True)