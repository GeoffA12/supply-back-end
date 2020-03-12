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
            (12345, 'Inactive', 'qw3256', 34, ' Toyota', 'V-9', 23.42, 42.12,),
            (13579, 'Active', 'gf9012', 34, 'Mercedes', 'V-9', 102.43, 231.12,),
            (12345, 'Active', 'qw3256', 34, 'Toyota', 'V-10', 12.51, 87.51,),
            (12345, 'Maintenance', 'qw3256', 34, 'Toyota', 'V-8', 23.42, 124.31,)
            )
    
    def getOrder(self):
        return {
            'orderID': 1234,
            'customerID': 42131,
            'serviceType': ServiceType.DRYCLEANING,
            'destination': {
                'lat': 12.53,
                'lon': 81.31
                },
            'timeOrderMade': '12:23:43',
            }
    
    def test_createdispatch(self):
        order = self.getOrder()
        vehicles = self.getVehicles()
        
        filteredVehicles = list(filter(lambda x: x[1] == 'Active', vehicles))
        print(filteredVehicles)
        vehicle = filteredVehicles[0]
        
        # Capture vehicle tuple into its separate variables
        vid, status, licensePlate, fleetId, make, model, vLon, vLat = vehicle
        
        # Seeing if the unpacking worked d:
        print(vehicle)
        print(vid)
        print(status)
        print(licensePlate)
        print(fleetId)
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
                'lon': vLon,
                'lat': vLat
                },
            }
        
        print(vehicleDict)
        dispatchDict = deepcopy(order)
        dispatchDict['vid'] = vid
        
        # Turn a destination dictionary into a tupled pair
        destination = dispatchDict.pop('destination')
        
        dispatchDict['loc_f'] = (destination['lat'], destination['lon'])
        dispatchDict['loc_0'] = (vLat, vLon)
        
        print(dispatchDict)
        
        dispatch = Dispatch(**dispatchDict)
        
        self.assertEqual(ServiceType.DRYCLEANING, dispatch.sType)
        self.assertEqual(13579, dispatch.vid)
        self.assertEqual(42131, dispatch.cid)
        self.assertEqual(1234, dispatch.oid)
        self.assertEqual((231.12, 102.43), dispatch.loc_0)
        self.assertEqual((12.53, 81.31), dispatch.loc_f)
        self.assertEqual(datetime.strptime("12:23:43", '%H:%M:%S').time(), dispatch.timeCreated)
        self.assertEqual(DispatchStatus.QUEUED, dispatch.status)
        print(dispatch)
        # print(type(dispatch.status))
        print(
                dispatch.sType, dispatch.vid,
                dispatch.cid, dispatch.oid,
                dispatch.loc_0[0], dispatch.loc_0[1],
                dispatch.loc_f[0], dispatch.loc_f[1],
                dispatch.timeCreated, dispatch.status
                )


if __name__ == '__main__':
    unittest.main()
