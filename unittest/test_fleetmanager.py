import unittest
import sys

sys.path.insert(1, '../')
from fleetmanager import FleetManager

postBody = {
    'username': 'komoto415',
    'email': 'komoto415@gmail.com',
    'password': 'password',
    'firstname': 'Jeffrey',
    'lastname': 'Ng',
    'phonenumber': '1234567890'
    }

class MyTestCase(unittest.TestCase):
    def test_createFleetManager(self):
        fm = FleetManager(**postBody)
        print(fm)
        self.assertEqual('komoto415', fm.username)
        self.assertEqual('Yes', fm.fleetIDs)

if __name__ == '__main__':
    unittest.main()
