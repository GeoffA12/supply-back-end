# Vehicle Request API Design

## HTTP Method Familiarity
| Method    | URI         | Action (CRUD)     | Has Request Body?
|:---       |:---         |:---               |:---
|POST       |/vehicles    |CREATE             |Yes
|PUT        |/vehicles    |UPDATE             |Yes
|PATCH      |/vehicles    |UPDATE (partial)   |Yes
|GET        |/vehicles    |READ               |No
|DELETE     |/vehicles    |DELETE             |No
|HEAD       |/vehicles    |EXISTS             |No

## Resources
| Parameter | Semantics     |
|:---       |:---           |
|oid        |Order ID       |
|vid        |Vehicle ID     |
|user       |Fleet master   |


### By Order ID ![Generic badge](https://img.shields.io/badge/status-Unstable-red.svg)
**API Call:**\
http://team22.supply.softwareengineeringii.com/vehiclesRequest/?oid={order id}
**Example API Call:**\
http://team22.supply.softwareengineeringii.com/vehiclesRequest/?oid={12}


### By Vehicle ID ![Generic badge](https://img.shields.io/badge/status-Stable-green.svg)
**API Call:**\
http://team22.supply.softwareengineeringii.com/vehiclesRequest/?vid={vehicle id}
**Example API Call:**\
http://team22.supply.softwareengineeringii.com/vehiclesRequest/?vid=30

### By Fleet Master ![Generic badge](https://img.shields.io/badge/status-Stable-green.svg)
**API Call:**\
http://team22.supply.softwareengineeringii.com/vehiclesRequest/?user={fleet master email}
**Example API Call:**\
http://team22.supply.softwareengineeringii.com/vehiclesRequest/?user='komoto415@gmail.com'

### By Fleet Number ![Generic badge](https://img.shields.io/badge/status-Unstable-red.svg)
**API Call:**\
http://team22.supply.softwareengineeringii.com/vehiclesRequest/?user={fleet master email}
**Example API Call:**\
http://team22.supply.softwareengineeringii.com/vehiclesRequest/?user='komoto415@gmail.com'

## Scenarios
**Generic GET Response**
This is a generic response of a get method to our API given that our client doesn't 
```
method: GET
URI: http://team22.supply.softwareengineeringii.com/vehicleRequest
[
    {
        "vehicleid": 38,
        "status": "inactive",
        "licenseplate": "MP4891",
        "fleetid": 5,
        "make": "Toyota",
        "model": "V-9",
        "current_lat": 30.2264,
        "current_lon": 97.7553,
        "last_heartbeat": null,
        "date_added": "2020-04-03T00:00:00"
    },
    {
        "vehicleid": 39,
        "status": "inactive",
        "licenseplate": "a",
        "fleetid": 1,
        "make": "a",
        "model": "a",
        "current_lat": 30.2264,
        "current_lon": 97.7553,
        "last_heartbeat": null,
        "date_added": "2020-04-03T23:06:35"
    }, ... , {
        n-th vehicle entry
    },
]
```

**Scenario 1:**\
Customer submits an order request
I the API am expecting an order.json from the DemandBE
I will respond to the DemandBE with confirmation of the order and that fulfillment has begun
```
method: POST 
URI: http://team22.supply.softwareengineeringii.com/vehicleRequest
Content-Type: application/json;

# Body as a JSON
# What I, the API, want to reviece as far as formatting is concerned
{
    'serviceType': 'DRYCLEANING',
    'custid': 1234567,
    'orderid': 1234,
    'destination': {
        'lat': 123,
        'lon': 123
        },
    'timeOrderMade': '2018-03-29T13:34:00.000'
}

# Some logic about deciding which vehicle gets selected. Vehicle gets selected
# Dispatch created. Strip order.json for all relevant data used for dispatch
    # Dispatch written to disaptchRecord table
    # Get some sort of route from mapping service
    # Car begins route (not really logic that happens here, just what probably happens next)

What I am expecting in my response (at the very least):
dest address
vehicle location
serviceType
isVehicleAvailable 
# I will now responde to the DemandDB with:
200 HTTPS Status
{

}
```

**Scenario 2:**\
The fleet manager wants to see what vehicle is fulfilling order 123
```
method: GET 
URI: http://team22.supply.softwareengineeringii.com/api/backend/0.0/vehicles?oid=123
No body associate with GET method. Just queries

Should be very similar, if not the exact same as the POST's response to the DemandBE.
However, depending how many parameters we might want to allow, it may restrict and/or append more data to our response.

# My response:
Expected HTTP Status: 200
{
    "vid" : 12345,
    "serviceType" : DryCleaning,
    "vehicleMake" : "Toyota",
    "liscencePlate" : "QW3456",
    "status" : Delivering,
    "location" : {
        "lon" : 23.42,
        "lat" : 42.12,
    },
    "destination" : {
        "address1" : "3001 S Congress Ave",
        "address2" : "St. Andres RM222D"
    }
}
```

**Scenario 3:**\
Our vehicle will periodically be sending its location and status. 
Since our status is now fulfilled, destination would be null/empty string (whatever gets decided for empty
  cells, for now will represent with empty strings)
```
method: PATCH 
URI: http://team22.supply.softwareengineeringii.com/api/backend/0.0/vehicles?vid=12345
Content-Type: application/json

I am the vehicle sending this JSON Body to the SupplyBE
{
    "status" : Delivered,
    "location" : {
        "lon" : 134.12,
        "lat" : 31.21
    },
    "destination" : {
        "address1" : "",
        "address2" : ""
    }
}

# Check for malformed data, query vehicle table on incoming VIN, PATCH incoming data
# Kinda rusty on SQL syntax, but I think this gets the message accross
def vehiclePing(self, desiredVIN, patchData)
    SELECT * FROM Vehicles WHERE VIN = desiredVIN:
    PATCH status, lon, lat, destination:
    patchData[status], 
    patchData[location[lon]], 
    patchData[location[lat]], 
    f'{patchData[destination[address1]]}, 
    {patchData[destination[address2]]}'
```