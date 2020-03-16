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
| Parameter | Semantics  |
|:---       |:---        |
|oid        |Order ID    |
|vin        |Vehicle IdN |

### By Order ID
**API Call:**\
http://team22.supply.softwareengineeringii.com/api/backend/0.0/vehicles?oid={order id}&appid={your api key}\
**Example API Call:**\
http://team22.supply.softwareengineeringii.com/api/backend/0.0/vehicles?oid=123

### By Vehicle Identification Number
**API Call:**\
http://team22.supply.softwareengineeringii.com/api/backend/0.0/vehicles?vin={order id}&appid={your api key}\
**Example API Call:**\
http://team22.supply.softwareengineeringii.com/api/backend/0.0/vehicles?vin=1WUYDCJE9FN072354

## Scenarios and Pseudocode of logic (Potential Test Cases!)
**Generic GET Response**
This is a generic response of a get method to our API given that our client doesn't 
```
method: GET
URI: http://team22.supply.softwareengineeringii.com/api/backend/0.0/vehicles
[
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
    },
    {
        "vid" : 98765,
        "serviceType" : PartyPlanner,
        "vehicleMake" : "Tesla",
        "liscencePlate" : "TE1241",
        "status" : Delivered,
        "location" : {
            "lon" : 45.12,
            "lat" : 10.31,
        },
        "destination" : {
            "address1" : "",
            "address2" : ""
        }
    },...,{nth vehicle data}
]
```

**Scenario 1:**\
Customer submits an order request
I the API am expecting an order.json from the DemandBE
I will respond to the DemandBE with confirmation of the order and that fulfillment has begun
```
method: POST 
URI: http://team22.supply.softwareengineeringii.com/api/backend/0.0/vehicles
Content-Type: application/json;

# Body as a JSON
# What I, the API, am receiving
{
    "serviceType" : DryCleaning",  # Could probably be an ENUM
    "cusomterID : 19821
    "orderID" : 123,
    "location" : {
        "lon" : 45.12,
        "lat" : 124.22
    },
    "timeOrderMade" : 12:02:34    # should be type DateTime
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