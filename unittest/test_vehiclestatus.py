import unittest
import sys

sys.path.insert(1, '../')
from enums.vehiclestatus import VehicleStatus


class MyTestCase(unittest.TestCase):
    
    def test_stringToEnum(self):
        enum = VehicleStatus.translate('active')
        self.assertEqual(VehicleStatus.ACTIVE, enum)
        enum = VehicleStatus.translate('AcTiVe')
        self.assertEqual(VehicleStatus.ACTIVE, enum)
        enum = VehicleStatus.translate('ACTIVE')
        self.assertEqual(VehicleStatus.ACTIVE, enum)
        enum = VehicleStatus.translate('aslkdas')
        self.assertEqual(None, enum)
    
    def test_active(self):
        enum = VehicleStatus.ACTIVE
        self.assertEqual('ACTIVE', enum.name)
        self.assertEqual(1, enum.value)
    
    def test_inactive(self):
        enum = VehicleStatus.INACTIVE
        self.assertEqual('INACTIVE', enum.name)
        self.assertEqual(2, enum.value)
    
    def test_maintenance(self):
        enum = VehicleStatus.MAINTENANCE
        self.assertEqual('MAINTENANCE', enum.name)
        self.assertEqual(3, enum.value)


if __name__ == '__main__':
    unittest.main()
