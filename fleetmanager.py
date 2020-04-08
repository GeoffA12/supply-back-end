# from utils.serverutils import connectToSQLDB
import sys

if '../' in sys.path[1]:
    sys.path[1] = sys.path[1] + '../common-services'
else:
    sys.path.insert(1, '../common-services')
# print(sys.path)

from account import Account


class FleetManager(Account):
    ver = '0.0.0'
    
    def __init__(self, username, email, password, firstname, lastname, phonenumber):
        super().__init__(username, email, password, firstname, lastname, phonenumber)
        self._fleetIDs = self.__fetchAssociatedFleetIDs()
    
    def __fetchAssociatedFleetIDs(self):
        print()
        return 'Yes'
    
    @property
    def fleetIDs(self):
        return self._fleetIDs
    
    def __str__(self):
        return f'''Username: {self._username}
Email: {self._email}
Password: {self._password}
First Name: {self._firstname}
Last Name: {self._lastname}
Phone Number: {self._phonenumber}
FleetIDs: {self._fleetIDs}
'''
