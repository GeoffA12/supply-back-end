import unittest
import sys

sys.path.insert(1, '../')
from ENUMS.servicetype import type

class MyTestCase(unittest.TestCase):

    def test_drycleaning(self):
        self.assertEqual('drycleaning', type.DRYCLEANING.value)
        self.assertTrue(isinstance(type.DRYCLEANING, type))
        print(type.DRYCLEANING.name)

    def test_rx(self):
        self.assertEqual('rx', type.RX.value)
        self.assertTrue(isinstance(type.RX, type))
        print(type.RX.name)

    def test_coffee(self):
        self.assertEqual('coffee', type.COFFEE.value)
        self.assertTrue(isinstance(type.COFFEE, type))
        print(type.COFFEE.name)

    def test_events(self):
        self.assertEqual('events', type.EVENTS.value)
        self.assertTrue(isinstance(type.EVENTS, type))
        print(type.EVENTS.name)

if __name__ == '__main__':
    unittest.main()
