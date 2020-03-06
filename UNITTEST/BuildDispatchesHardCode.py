import unittest
import copy
import sys

sys.path.insert(1, '../')
from dispatch import Dispatch

class TestDispatch(unittest.TestCase):

    def getVehicles(self):
        return (
            (12345, 'Inactive', 'qw3256', 34, ' Toyota', 'V-9', 23.42, 42.12,),
            (13579, 'Active', 'gf9012', 34, 'Mercedes', 'V-9', 102.43, 231.12,),
            (12345, 'Active', 'qw3256', 34, 'Toyota', 'V-10', 12.51, 87.51,),
            (12345, 'Maintenance', 'qw3256', 34, 'Toyota', 'V-8', 23.42, 124.31,)
        )

    def getOrder(self):
        return {
            'orderID': 1234,
            'customerID': 42131,
            'serviceType': 'DryCleaning',
            'destination': {
                'lon': 123.12,
                'lat': 51.12
            },
            'timeOrderMade': '12:23:43',
        }


    def test_createDispatch(self):
        vehicles = self.getVehicles()
        order = self.getOrder()

        filteredVehicles = list(filter(lambda x: x[1] == 'Active', vehicles))
        vehicle = filteredVehicles[0]

        vid, status, liscensePlate, fleetId, make, model, vLon, vLat = vehicle

        dispatchDict = copy.deepcopy(order);
        dispatchDict['vid'] = vid

        # Turn a destination dictionary into a tupled pair
        attrToTuple = dispatchDict.pop('destination');

        dispatchDict['loc_f'] = (attrToTuple['lon'], attrToTuple['lat'])
        dispatchDict['loc_0'] = (vLon, vLat)

        dispatch = Dispatch(**dispatchDict)

        print(dispatch)
        print(type(dispatch.status))

if __name__ == '__main__':
    unittest.main()