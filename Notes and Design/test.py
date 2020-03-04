from dispatch import Dispatch
import copy
def main():
    vehicles = (
        (12345, 'Inactive',     'qw3256',   34,   ' Toyota',    'V-9',      23.42,  42.12,),
        (13579, 'Active',       'gf9012',   34,    'Mercedes', 'V-9',      102.43, 231.12, ),
        (12345, 'Active',       'qw3256',   34,     'Toyota',   'V-10',     12.51,  87.51, ),
        (12345, 'Maintenance',  'qw3256',   34,     'Toyota',   'V-8',      23.42,  124.31, )
    )

    order = {
        'orderID' : 1234,
        'customerID' : 42131,
        'serviceType' : 'DryCleaning',
        'destination' : {
            'lon' : 123.12,
            'lat' : 51.12
        },
        'timeOrderMade' : '12:23:43',
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


    # Capture vehicle tuple into its separate variables
    vid, status, liscensePlate, fleetId, make, model, vLon, vLat = vehicle

    # Seeing if the unpacking worked d:
    print(vehicle)
    print(vid)
    print(status)
    print(liscensePlate)
    print(fleetId)
    print(make)
    print(model)
    print(vLon)
    print(vLat)

    vehicleDict = {
        'vid' : vid,
        'status' :  'Active',
        'liscensePlate' : liscensePlate,
        'make' : make,
        'model' : model,
        'curLocation' : {
            'lon' : vLon,
            'lat' : vLat
        },
    }

    print(vehicleDict)

    # Deep copy the dictionary because we'll need to mutate what's in here a bit. Also separates this from the already
    # existing containers floating around
    dispatchDict = copy.deepcopy(order);
    dispatchDict['vid'] = vid

    # Turn a destination dictionary into a tupled pair
    attrToTuple = dispatchDict.pop('destination');
    print(attrToTuple)
    dispatchDict['loc_f'] = (attrToTuple['lon'], attrToTuple['lat'])
    dispatchDict['loc_0'] = (vLon, vLat)

    print(dispatchDict)

    dispatch = Dispatch(**dispatchDict)

    print(dispatch)

if __name__ == '__main__':
    main()