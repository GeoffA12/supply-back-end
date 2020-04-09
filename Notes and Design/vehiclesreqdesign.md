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

## Read Supported Vehicle Resources
TO BE REFACTORED  
URI: `/vehicleRequest`

| Parameter | Semantics     |
|:---       |:---           |
|vid        |Vehicle ID     |   
|oid        |Order ID       |
|fmid       |Fleet master   |
|fid        |Fleet ID       |

### By Vehicle ID ![Generic badge](https://img.shields.io/badge/status-Stable-green.svg)
**API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?vid={vehicle id}  
**Example API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?vid=30

### By Order ID ![Generic badge](https://img.shields.io/badge/status-Unstable-red.svg)
**API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?oid={order id}  
**Example API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?oid=12

### By Fleet Master ![Generic badge](https://img.shields.io/badge/status-Stable-green.svg)
**API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?fmid={fleet master email}  
**Example API Call:**  
https://supply.team22.softwareengineeringii.com/supply/vehicles?fmid=komoto415%40gmail.com

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

## Read Supported Dispatch Resources
TO BE REFACTORED  
URI: `/getDispatch`

| Parameter | Semantics     |
|:---       |:---           |
|vid        |Vehicle ID     |

### By Vehicle ID ![Generic badge](https://img.shields.io/badge/status-Stable-green.svg)
**API Call:**  
https://supply.team22.softwareengineeringii.com/supply/dispatch?vid={order id}  
**Example API Call:**  
https://supply.team22.softwareengineeringii.com/supply/dispatch?vid=12  

## Scenarios


## POST Supported Resources
|URI                    |Semantics
|:---                   |:---
|/supply/vehicles/req   |Request a vehicle (on order)
|/supply/vehicles/add   |Added a vehicle
|/supply/vehicles/rem   |Remove a vehicle
|/supply/vehicles/upd   |Update a vehicle

### Vehicle Request
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
```python
# method: POST 
# URI: https://supply.team22.softwareengineeringii.com/vehicles/req
# Content-Type: application/json;

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

# What I will be responding with as a json():
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

### Registering a Vehicle
Keys Value Constraints of the post body ***case sensitive**:

|Key            |Value Type
|:---           |:---
|fleetid        |String
|make           |String
|model          |String
|licensePlate   |String
|dateAdded      |String

In addition to the key value constraints, multiple simultaneous vehicle registration is supported. Each vehicle
 dictionary will be contained inside of an array, even in the case of adding a single vehicle

#### Example acceptable postBody
```python
postBody = [
    {
        'fleetid': '8',
        'make': 'Honda',
        'model': 'Civic',
        'licensePlate': 'AZ4915',
        'dateAdded': '2020-03-28T08:34:32.698Z'
    }
]
```
**Scenario**
A Fleet manager adds some vehicles to his fleet
```python
# method: POST 
# URI: https://supply.team22.softwareengineeringii.com/vehicles/add
# Content-Type: application/json;
{
    'fleetid': '8',
    'make': 'Honda',
    'model': 'Civic',
    'licensePlate': 'AZ4915',
    'dateAdded': '2020-03-28T08:34:32.698Z'
}
```
### Removing a Vehicle

### Updating a Vehicle
Keys Value Constraints of the post body ***case sensitive**:

|Key                |Value Type
|:---               |:---
|vid*               |String
|status*            |String
|licenseplate       |String
|fleetid            |String
|current_lat        |Float
|current_lon        |Float
|last_heartbeat*    |String

#### *Notes for Key Value Constraints
##### vid
Every update request MUST have the vid key

##### last_heartbeat
The formatting of the heartbeat must be in ISO 8601 format
Given that the last_heartbeat key exists, postBody must also contain the keys current_lat and current_lon

#### Example acceptable postBody
```python
postBody = {
    'vid': '23',
    'status': 'MAINTENANCE'
}
```
**Scenario**
A vehicle sends its heartbeat
```python
# method: POST 
# URI: https://supply.team22.softwareengineeringii.com/vehicles/upd
# Content-Type: application/json;
{
    'vid': '23',
    'current_lat': 51.51,
    'current_lon': -12.41, 
    'last_heartbeat': '2020-04-07T11:54:12.698Z'
}
```