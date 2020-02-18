# Vehicle Request API Design

## HTTP Method Familiarity
| Method    | URI                  | Action (CRUD)     | Has Request Body?
|:---       |:---                  |:---               |:---
|POST       |/vehicles             |CREATE             |Yes
|PUT        |/vehicles/vin/123     |UPDATE             |Yes
|PATCH      |/vehicles/vin/123     |UPDATE (partial)   |Yes
|GET        |/vehicles?vin=123     |READ               |No
|DELETE     |/vehicles?vin=123     |DELETE             |No
|HEAD       |/vehicles?vin=123     |EXISTS             |No

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
    "serviceType" : "dryCleaning",  # Could probably be an ENUM
    "orderID" : 123,
    "destination" : {
        "address1" : "3001 S Congress Ave",
        "address2" : "St. Andres 222D"
    },
    "phoneNum" : 9728002591,
    "timeOrderMade" : 12:02:34    # should be type DateTime or Timestamp(<-- only SQL?)
}

# Some logic about deciding which vehicle gets selected. Vehicle gets selected
# Dispatch created
    # Dispatch written to disaptchRecord table
    # Get some sort of route from mapping service
    # Car begins route (not really logic that happens here, just what probably happens next)

What I am expecting in my response (at the very least):
dest address
vehicle location
serviceType
isVehicleAvailable 
# I will now responde to the DemandDB with
```

The fleet manager wants to see what vehicle is fulfilling order 123
```
method: GET 
URI: http://team22.supply.softwareengineeringii.com/api/backend/0.0/vehicles?oid=123
No body associate with GET method. Just queries

Should be very similar, if not the exact same as the POST's response to the DemandBE.
However, depending how many parameters we might want to allow, it may restrict and/or append more data to our response.
Below will be generic response given oid

# My response:
Expected HTTP Status: 200
{
    "VIN" : "1WUYDCJE9FN072354",
    "serviceType" : DryCleaning
    "vehicleMake" : "Toyota",
    "liscencePlate" : "QW3456",
    "status" : "Fulfilling"
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

Our vehicle will periodically be sending its location and status. 
In this case the most important change will be that the current dispatch has been completed and order delivered. And
 since there is now order being fulfilled, destination would be null/empty string (whatever gets decided for empty
  cells, for now will represent with empty strings)
```
method: PATCH 
URI http://team22.supply.softwareengineeringii.com/api/backend/0.0/vehicles?vid="1WUYDCJE9FN072354"
Content-Type: application/json

I am the vehicle sending this JSON Body to the SupplyBE
{
    "status" : "Delivered",
    "location" : {
        "lon" : 134.12,
        "lat" : 31.21,
    },
    "destination" : {
        "address1" : "",
        "address2" : ""
    }
}

def PATCH(self)
    if(path == ./carData)
        Update vehicle table with new coordinates and status
```

| HTTP Code | POST condition                            | GET condition
|:---       |:---                                       |:---
|201        |Order confirmed, and vehicle dispatched    |
|400        |Order.json is malformed (demand end?)      |
|404        |Resource not found                         |