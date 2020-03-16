import unittest
import sys

sys.path.insert(1, '../')
from enums.vehiclestatus import VehicleStatus


class MyTestCase(unittest.TestCase):
    
    def test_active(self):
        self.assertEqual('active', VehicleStatus.ACTIVE.value)
        self.assertTrue(isinstance(VehicleStatus.ACTIVE, VehicleStatus))
        print(VehicleStatus.ACTIVE.name)
    
    def test_inactive(self):
        self.assertEqual('inactive', VehicleStatus.INACTIVE.value)
        self.assertTrue(isinstance(VehicleStatus.INACTIVE, VehicleStatus))
        print(VehicleStatus.INACTIVE.name)
    
    def test_maintenance(self):
        self.assertEqual('maintenance', VehicleStatus.MAINTENANCE.value)
        self.assertTrue(isinstance(VehicleStatus.MAINTENANCE, VehicleStatus))
        print(VehicleStatus.MAINTENANCE.name)


if __name__ == '__main__':
    unittest.main()
