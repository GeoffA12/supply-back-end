import random
from dispatch import Dispatch
def main():
    # vehicles = [
    #     {
    #         "vid": 12345,
    #         "serviceType": "DryCleaning",
    #         "vehicleMake": "Toyota",
    #         "liscencePlate": "QW3456",
    #         "status": "Active",
    #         "location": {
    #             "lon": 23.42,
    #             "lat": 42.12,
    #         },
    #         "destination": {
    #             "lon": 13.12,
    #             "lat": 112.61
    #         }
    #     },
    #     {
    #         "vid": 98765,
    #         "serviceType": "PartyPlanner",
    #         "vehicleMake": "Tesla",
    #         "liscencePlate": "TE1241",
    #         "status": "Inactive",
    #         "location": {
    #             "lon": 45.12,
    #             "lat": 10.31,
    #         },
    #         "destination": {
    #             "lon": None,
    #             "lat": None
    #         }
    #     }
    # ]

    vehicles = (
        (12345, 'Inactive',     'qw3256',   34,   ' Toyota',    'V-9',      23.42,  42.12,),
        (13579, 'Active',       'gf9012',   34,    'Merdeces', 'V-9',      102.43, 231.12, ),
        (12345, 'Active',       'qw3256',   34,     'Toyota',   'V-10',     12.51,  87.51, ),
        (12345, 'Maintenance',  'qw3256',   34,     'Toyota',   'V-8',      23.42,  124.31, )
    )

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

    '''
    Steps.
    1) Receive a JSON body of the order made by the customer
    2) Query for vehicles who have their status as Available and whose fleet ID matches the service Type
    3) Convert vehicle tuple (what gets returned in a cursor.fetch) into a dictionary (can probably be a helper method)
    4) From order.json, convert destination from dictionary individual variables for DB write
    
    '''
    # For now assuming all in the same fleet and fleet matches serviceType of order
    filteredVehicles = list(filter(lambda x: x[1] == 'Active', vehicles))
    print(filteredVehicles)
    vehicle = filteredVehicles[0]

    vid, status, liscensePlate, fleetId, make, model, lon, lat = vehicle

    print(vehicle)
    print(vid)
    print(status)
    print(liscensePlate)
    print(fleetId)
    print(make)
    print(model)
    print(lon)
    print(lat)

if __name__ == '__main__':
    main()