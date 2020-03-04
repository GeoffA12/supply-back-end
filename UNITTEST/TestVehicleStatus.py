import unittest
import sys

sys.path.insert(1, '../ENUMS/')

from vehiclestatus import status

class MyTestCase(unittest.TestCase):

    def test_active(self):
        self.assertEqual('active', status.ACTIVE.value)
        self.assertTrue(isinstance(status.ACTIVE, status))
        print(status.ACTIVE.name)

    def test_inactive(self):
        self.assertEqual('inactive', status.INACTIVE.value)
        self.assertTrue(isinstance(status.INACTIVE, status))
        print(status.INACTIVE.name)

    def test_maintenance(self):
        self.assertEqual('maintenance', status.MAINTENANCE.value)
        self.assertTrue(isinstance(status.MAINTENANCE, status))
        print(status.MAINTENANCE.name)


if __name__ == '__main__':
    unittest.main()
