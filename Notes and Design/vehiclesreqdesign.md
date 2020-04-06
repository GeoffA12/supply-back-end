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

## Read Supported Resources
TO BE REFACTORED  
URI: `/vehicleRequest`

| Parameter | Semantics     |
|:---       |:---           |
|oid        |Order ID       |
|vid        |Vehicle ID     |
|user       |Fleet master   |
|fid        |Fleet ID       |


### By Order ID ![Generic badge](https://img.shields.io/badge/status-Unstable-red.svg)
**API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?oid={order id}  
**Example API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?oid=12

### By Vehicle ID ![Generic badge](https://img.shields.io/badge/status-Stable-green.svg)
**API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?vid={vehicle id}  
**Example API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?vid=30

### By Fleet Master ![Generic badge](https://img.shields.io/badge/status-Stable-green.svg)
**API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?user={fleet master email}  
**Example API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?user=komoto415%40gmail.com

### By Fleet ID ![Generic badge](https://img.shields.io/badge/status-Broken-red.svg)
**API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?fid={fleet id}  
**Example API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?fid=8

## Scenarios
**Generic GET Response**
This is a generic response of a get method to our API given that our client doesn't 
```
method: GET
URI: https://supply.team22.softwareengineeringii.com/supply/vehicles
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
**Scenario:**  
The fleet manager wants to see what vehicle is fulfilling order 123
```
method: GET 
URI: https://supply.team22.softwareengineeringii.com/supply/vehicles?oid=123

if there is a dispatch that has the order id 123 and is either running or queued
HTTP Status: 200
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

else:
HTTP Status: 404
{
    'failed': f'No running dispatch with order id {oid}'
}
```

## POST Supported Resources
|URI                                |Semantics
|:---                               |:---
|[/supply/vehicles/req](#vreq)      |Request a vehicle (on order)
|[/supply/vehicles/add](#vadd)      |Added a vehicle
|[/supply/vehicles/rem](#vrem)      |Remove a vehicle
|[/supply/vehicles/upd](#vupd)      |Update a vehicle

<a id="vreq"></a> 
###Vehicle Request
Keys Value Constraints of the post body ***case sensitive**:

|Key            |Value Type
|:---           |:---
|serviceType*   |String
|custid         |Integer
|orderid        |Integer
|destination*   |Dictionary
|timeOrderMade  |String

#### *Notes for Key Value Constraints
##### serviceType:
The value of said string will be derived from ServiceType enumerated type name attribute. Provided in the ServiceType
 enum is a translate method that will check only casings and translate into the appropriate enum. Failure of
  translation may be indicative of the fact that we do no provide whatever the service you are trying to enumerate.
 
Example: 
```python
st = 'DrYcLeaning'
serviceTypeEnum = ServiceType.translate(st)
print(serviceTypeEnum)    
print(serviceTypeEnum.name)
``` 
Output:
```
ServiceType.DRYCLEANING
DRYCLEANING
```

##### destination
Keys Value Constraints of the destination key's value ***case sensitive**:

|Key    |Value Type
|:---   |:---
|lat    |Float
|lon    |Float

Example of acceptable destination key value:
```python
postBody['destination'] = {
    'lat': 12.521,
    'lon': 35.413
}
```

#### Example acceptable postBody
```python
postBody = {
    'serviceType': 'DRYCLEANING',
    'custid': 1234567,
    'orderid': 1234,
    'destination': {
        'lat': 12.521,
        'lon': 35.413
        },
    'timeOrderMade': '2018-03-29T13:34:00.000'
}
```
**Scenario:**  
Customer submits an order request
I the API am expecting an order.json from the DemandBE
I will respond to the DemandBE with confirmation of the order and that fulfillment has begun
```
method: POST 
URI: https://supply.team22.softwareengineeringii.com/vehicles/req
Content-Type: application/json;

# Body as a JSON
# What I, the API, want to reviece as far as formatting is concerned
{
    'serviceType': 'DRYCLEANING',
    'custid': 1234567,
    'orderid': 1234,
    'destination': {
        'lat': 12.521,
        'lon': 35.413
        },
    'timeOrderMade': '2018-03-29T13:34:00.000'
}

# Some logic about deciding which vehicle gets selected
# Dispatch written to disaptchRecord table
# Get some sort of route from mapping service


What I will be responding with as a json():
{
    'vid': vid,
    'licensePlate': licensePlate,
    'make': make,
    'model': model,
    'curLocation': {
        'lat': vLat,
        'lon': vLon
        },
    'eta': eta
}

```

<a id="vadd"><a/>
### Registering a Vehicle

<a id="vrem"><a/>
### Removing a Vehicle

<a id="vupd"><a/>
### Updating a Vehicle

Need to revise  
**Scenario 3:**  
Our vehicle will periodically be sending its location and status. 
Since our status is now fulfilled, destination would be null/empty string (whatever gets decided for empty
  cells, for now will represent with empty strings)
```
method: PATCH 
URI: https://supply.team22.softwareengineeringii.com/api/backend/0.0/vehicles?vid=12345
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