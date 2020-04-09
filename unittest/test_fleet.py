import unittest
import sys

sys.path.insert(1, '../')
from fleet import Fleet
from enums.servicetype import ServiceType


class MyTestCase(unittest.TestCase):
    def test_createfleet(self):
        fleet = Fleet(123, 12, 'Austin', ServiceType.COFFEE)

        self.assertEqual(123, fleet.fleetid)
        self.assertEqual(12, fleet.fmid)
        self.assertEqual('Austin', fleet.region)
        self.assertEqual(ServiceType.COFFEE, fleet.serviceType)

        print(fleet)
        print()

        print(repr(fleet))
        print()


if __name__ == '__main__':
    unittest.main()
