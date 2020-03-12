import unittest
import sys

sys.path.insert(1, '../')
from enums.servicetype import ServiceType


class MyTestCase(unittest.TestCase):
    
    def test_drycleaning(self):
        self.assertEqual('drycleaning', ServiceType.DRYCLEANING.value)
        self.assertTrue(isinstance(ServiceType.DRYCLEANING, ServiceType))
        print(ServiceType.DRYCLEANING.name)
    
    def test_rx(self):
        self.assertEqual('rx', ServiceType.RX.value)
        self.assertTrue(isinstance(ServiceType.RX, ServiceType))
        print(ServiceType.RX.name)
    
    def test_coffee(self):
        self.assertEqual('coffee', ServiceType.COFFEE.value)
        self.assertTrue(isinstance(ServiceType.COFFEE, ServiceType))
        print(ServiceType.COFFEE.name)
    
    def test_events(self):
        self.assertEqual('events', ServiceType.EVENTS.value)
        self.assertTrue(isinstance(ServiceType.EVENTS, ServiceType))
        print(ServiceType.EVENTS.name)


if __name__ == '__main__':
    unittest.main()
