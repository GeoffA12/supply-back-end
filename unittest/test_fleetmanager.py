import unittest
import sys
from copy import deepcopy

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
        
        self.assertEqual('komoto415', fm.username)
        self.assertEqual('komoto415@gmail.com', fm.email)
        self.assertEqual('password', fm.password)
        self.assertEqual('Jeffrey', fm.firstname)
        self.assertEqual('Ng', fm.lastname)
        self.assertEqual('1234567890', fm.phonenumber)
        self.assertEqual('Yes', fm.fleetIDs)
        
        print(fm)
        print()
        
        print(repr(fm))
        print()
    
    def test_failedToCreateByEmail(self):
        postBodyCopy = deepcopy(postBody)
        postBodyCopy['email'] = 'komoto415.com'
        try:
            fm = FleetManager(**postBodyCopy)
        except ValueError as ve:
            print(ve)
            print('Yay! We hit hit a ValueError')
        print()
    
    def test_failedToCreateByPassword(self):
        postBodyCopy = deepcopy(postBody)
        postBodyCopy['password'] = '123'
        try:
            fm = FleetManager(**postBodyCopy)
        except ValueError as ve:
            print(ve)
            print('Yay! We hit hit a ValueError')
        print()


if __name__ == '__main__':
    unittest.main()
