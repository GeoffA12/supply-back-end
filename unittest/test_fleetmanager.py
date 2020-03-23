import unittest
import sys

sys.path.insert(1, '../')
from fleetmanager import FleetManager


class MyTestCase(unittest.TestCase):
    def test_createFleetManager(self):
        fm = FleetManager('user1')
        
        self.assertEqual('user1', fm.username)
        self.assertEqual(123, fm.fmid)
        self.assertEqual('email1@gmail.com', fm.email)
        self.assertTrue(1 in fm.fleetids)
        self.assertFalse(3 in fm.fleetids)
        
        print(fm)


if __name__ == '__main__':
    unittest.main()
