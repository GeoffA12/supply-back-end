import unittest
from copy import deepcopy
from datetime import datetime
import sys

sys.path.insert(1, '../')
from dispatch import Dispatch
from enums.servicetype import ServiceType
from enums.dispatchstatus import DispatchStatus


class TestDispatch(unittest.TestCase):

    def getVehicles(self):
        return (
            (12345, 'qw3256', 'Toyota', 'V-9', 23.42, 42.12,),
            (13579, 'gf9012', 'Mercedes', 'V-9', 102.43, 231.12,),
            (12345, 'qw3256', 'Toyota', 'V-10', 12.51, 87.51,),
            (12345, 'qw3256', 'Toyota', 'V-8', 23.42, 124.31,)
        )

    def getDCOrder(self):
        return {
            'serviceType': ServiceType.DRY_CLEANING.name,
            'custid': 1234567,
            'orderid': 1234,
            'destination': {
                'lat': 31,
                'lon': 12
            },
            'timeOrderMade': "2020-03-29T13:34:00.000"
        }

    def test_createDCdispatch(self):
        order = self.getDCOrder()
        vehicles = self.getVehicles()
        vehicle = vehicles[0]
        order['serviceType'] = ServiceType.translate(order['serviceType'])
        # Capture vehicle tuple into its separate variables
        vid, licensePlate, make, model, vLat, vLon = vehicle

        # Seeing if the unpacking worked d:
        print(vehicle)
        print()

        print(vid)
        print(licensePlate)
        print(make)
        print(model)
        print(vLon)
        print(vLat)
        print()

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
        print()

        dispatchDict = deepcopy(order)
        dispatchDict['vid'] = vid

        # Turn a destination dictionary into a tupled pair
        destination = dispatchDict.pop('destination')

        dispatchDict['loc_f'] = (destination['lat'], destination['lon'])
        dispatchDict['loc_0'] = (vLat, vLon)

        # dispatchDict['status'] = DispatchStatus.RUNNING

        print(dispatchDict)
        print()

        dispatch = Dispatch(**dispatchDict)

        self.assertEqual(ServiceType.DRY_CLEANING, dispatch.serviceType)
        self.assertEqual(12345, dispatch.vid)
        self.assertEqual(1234567, dispatch.custid)
        self.assertEqual(1234, dispatch.orderid)
        self.assertEqual((23.42, 42.12), dispatch.loc_0)
        self.assertEqual((31, 12), dispatch.loc_f)
        self.assertEqual("2020-03-29T13:34:00.000", dispatch.timeCreated)
        self.assertEqual(DispatchStatus.RUNNING, dispatch.status)

        print(dispatch)
        print()
        self.assertEqual(2, dispatch.status.value)

        dispatch.completed()
        self.assertEqual(DispatchStatus.DONE, dispatch.status)
        print(dispatch)
        print()

        print(repr(dispatch))


if __name__ == '__main__':
    unittest.main()
