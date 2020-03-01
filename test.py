import random
from dispatch import Dispatch
def main():
    vehicles = [
        {
            "vid": 12345,
            "serviceType": "DryCleaning",
            "vehicleMake": "Toyota",
            "liscencePlate": "QW3456",
            "status": "Active",
            "location": {
                "lon": 23.42,
                "lat": 42.12,
            },
            "destination": {
                "address1": 13.12,
                "address2": 112.61
            }
        },
        {
            "vid": 98765,
            "serviceType": "PartyPlanner",
            "vehicleMake": "Tesla",
            "liscencePlate": "TE1241",
            "status": "Inactive",
            "location": {
                "lon": 45.12,
                "lat": 10.31,
            },
            "destination": {
                "address1": None,
                "address2": None
            }
        }
    ]

    order = {
        'orderId' : 1234,
        'custId' : 42131,
        'serviceType' : 'DryCleaning',
        'destination' : {
            'lon' : 123.12,
            'lat' : 51.12
        },
        'timeOrderCreated' : '12:23:43',
    }
    vehicle = vehicles[1];
    print(order)
    endPair = order.pop('destination')
    print(endPair)

    endLon = endPair['lon']
    endLat = endPair['lat']
    print(endLon, endLat)

    print(vehicle)

if __name__ == '__main__':
    main()