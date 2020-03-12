import unittest
import copy
import sys

sys.path.insert(1, '../')
from dispatch import Dispatch
from ENUMS.servicetype import ServiceType


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
            'serviceType': ServiceType.DRYCLEANING.value,
            'destination': "St. Edward's University",
            'timeOrderMade': '12:23:43',
            }
    
    def test_createDispatch(self):
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
            'liscensePlate': licensePlate,
            'make': make,
            'model': model,
            'curLocation': {
                'lon': vLon,
                'lat': vLat
                },
            }
    
        print(vehicleDict)
        dispatchDict = copy.deepcopy(order)
        dispatchDict['vid'] = vid
    
        attrToTuple = dispatchDict.pop('destination')
        print(attrToTuple)
    
        attrToTuple = {
            'lon': 123.12,
            'lat': 32.1
            }
    
        dispatchDict['loc_f'] = (attrToTuple['lon'], attrToTuple['lat'])
        dispatchDict['loc_0'] = (vLon, vLat)
    
        print(dispatchDict)
    
        dispatch = Dispatch(**dispatchDict)
    
        print(dispatch)
        # print(type(dispatch.status))
        print(
                dispatch.sType, dispatch.vid,
                dispatch.cid, dispatch.oid,
                dispatch.loc_0[1], dispatch.loc_0[0],
                dispatch.loc_f[1], dispatch.loc_f[0],
                dispatch.timeCreated, dispatch.status
                )


if __name__ == '__main__':
    unittest.main()
