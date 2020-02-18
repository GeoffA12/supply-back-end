## Vehicle Request API Design

### HTTP Verb Familiarity
| Method    | URI                  | Action (CRUD)     | Has Request Body?
|:---       |:---                  |:---               |:---
|POST       |/vehicles             |CREATE             |Yes
|PUT        |/vehicles?vin=123     |UPDATE             |Yes
|PATCH      |/vehicles?vin=123     |UPDATE (partial)   |Yes
|GET        |/vehicles?vin=123     |READ               |No
|DELETE     |/vehicles?vin=123     |DELETE             |No
|HEAD       |/vehicles?vin=123     |EXISTS             |No

### Resources

#### Parameters 
Potential Parameters for Vehicles

| Parameter | Symbolism         | GET             | UPDATE                       | DELETE
|:---       |:---               |:---             |:---                          |:---
|oid        |Order ID           |The order ID     |
|id         |Vehicle ID         |The vehicle ID   | 

Sample GET utilising the oid parameter
```
method: GET 
URI: http://team22.supply.softwareengineeringii.com/api/backend/vehicles?oid=123

What I am expecting in my reponse (at least):
dest address
vehicle location
serviceType
isVehicleAvailable 

# My reponse:
{
    "VIN" : "1WUYDCJE9FN072354",
    "serviceType" : DryCleaning
    "vehicleMake" : "Toyota",
    "liscencePlate" : "QW3456",
    "status" : "Fulfilling"
    "long" : 23.42,
    "lat" : 42.12,
    "destination" : {
        "address1" : "3001 S Congress Ave",
        "address2" : "St. Andres RM222D"
    }
}
```

#### Bodies
When our customer submits and order request, we are expecting an order.json
```
method: POST 
URI: http://team22.supply.softwareengineeringii.com/api/backend/vehicles
Content-Type: application/json;

# Body as a JSON
# What I, the API, am receiving
{
    "serviceType" : "dryCleaning",  # Could probably be an ENUM
    "customerID" : "12345",
    "address1" : "3001 S Congress Ave",
    "address2" : "St. Andres 222D",
    "phoneNum" : 9728002591,
    "time" : 12:02:34    # should be type DateTime or Timestamp(<-- only SQL?)
}
```

Our vehicle will periodically be sending some kind of telemetry updating us on its location, orderStatus,
and if its been dispatched or not.
```
method: PATCH 
URI http://team22.supply.softwareengineeringii.com/api/backend/vehicles?vid="1WUYDCJE9FN072354"
Content-Type: application/json

I am the vehicle sending this JSON Body to the SupplyBE
{
    "long" : 134.12,
    "lat" : 31.21
    "status" : Delivered
}

def PATCH(self)
    if(path == ./carData)
        Update vehicle table with new coordinates and status
```

| HTTP Code | Condition for code
|:---       |:---
|201        |Order was placed, given an ID, has been dispatched to a vehicle and vehicle begins fulfillment
|400        |Customers input were not formatted properly
|401        |Empty fields submitted
|404        |Resource not found