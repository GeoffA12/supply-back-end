import unittest
import sys

sys.path.insert(1, '../')
from fleet import Fleet
from enums.servicetype import ServiceType


class MyTestCase(unittest.TestCase):
    def test_createfleet(self):
        fleet = Fleet(123, 12, 'Austin', ServiceType.COFFEE)
        print(fleet)
        
        self.assertEqual(123, fleet.fleetid)
        self.assertEqual(12, fleet.fmid)
        self.assertEqual('Austin', fleet.region)
        self.assertEqual(ServiceType.COFFEE, fleet.sType)


if __name__ == '__main__':
    unittest.main()
