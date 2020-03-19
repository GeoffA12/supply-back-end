import unittest
from copy import deepcopy
from datetime import datetime
import sys

sys.path.insert(1, '../')
from dispatch import Dispatch
from enums.servicetype import ServiceType
from enums.dispatchstatus import DispatchStatus


class TestDispatch(unittest.TestCase):
    dispatch = None
    
    def getVehicles(self):
        return (
            (12345, 'qw3256', 'Toyota', 'V-9', 23.42, 42.12,),
            (13579, 'gf9012', 'Mercedes', 'V-9', 102.43, 231.12,),
            (12345, 'qw3256', 'Toyota', 'V-10', 12.51, 87.51,),
            (12345, 'qw3256', 'Toyota', 'V-8', 23.42, 124.31,)
            )
    
    def getOrder(self):
        return {
            'serviceType': ServiceType.DRY_CLEANING,
            'customerID': 1234567,
            'orderID': 1234,
            'destination': {
                'lat': 123,
                'lon': 123
                },
            'timeOrderMade': datetime(2011, 11, 4, 0, 5, 23)
            }
    
    def test_createdispatch(self):
        order = self.getOrder()
        vehicles = self.getVehicles()
        vehicle = vehicles[0]
        
        # Capture vehicle tuple into its separate variables
        vid, licensePlate, make, model, vLat, vLon = vehicle
        
        # Seeing if the unpacking worked d:
        print(vehicle)

        print(vid)
        print(licensePlate)
        print(make)
        print(model)
        print(vLon)
        print(vLat)
        
        vehicleDict = {
            'vid': vid,
            'licensePlate': licensePlate,
            'make': make,
            'model': model,
            'curLocation': {
                'lat': vLat,
                'lon': vLon
                },
            }

        print(vehicleDict)
        dispatchDict = deepcopy(order)
        dispatchDict['vid'] = vid

        # Turn a destination dictionary into a tupled pair
        destination = dispatchDict.pop('destination')

        dispatchDict['loc_f'] = (destination['lat'], destination['lon'])
        dispatchDict['loc_0'] = (vLat, vLon)

        # dispatchDict['status'] = DispatchStatus.RUNNING

        print(dispatchDict)

        dispatch = Dispatch(**dispatchDict)

        self.assertEqual(ServiceType.DRY_CLEANING, dispatch.serviceType)
        self.assertEqual(12345, dispatch.vid)
        self.assertEqual(1234567, dispatch.custid)
        self.assertEqual(1234, dispatch.orderid)
        self.assertEqual((23.42, 42.12), dispatch.loc_0)
        self.assertEqual((123, 123), dispatch.loc_f)
        self.assertEqual(datetime(2011, 11, 4, 0, 5, 23), dispatch.timeCreated)
        self.assertEqual(DispatchStatus.QUEUED, dispatch.status)

        print(dispatch)

        self.assertEqual(1, dispatch.status.value)


if __name__ == '__main__':
    unittest.main()
