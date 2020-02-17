## Test API Design

###Resources
#### Parameters
* `/orders?id=123`
* `/orders?service='drycleaning'`
* 

#### Orders

|Resource               |POST                           |GET                            
|:---                   |:---                           |:---                           
|/orders                |Create a new order             |Retrieve all orders           
|/orders/123            |Error                          |Retrieve details of order 123 
|                       |                               |                               

Example of `POST` with `/orders`
```HTTP
POST http://team22.supply.softwareengineeringii.com/orders
Content-Type: application/json;

# The JSON being sent
{
    "serviceType" : "dryCleaning",  # Could probably be an ENUM
    "customerID" : "12345",
    "address1" : "3001 S Congress Ave",
    "address2" : "St. Andres 222D",
    "phoneNum" : 9728002591
    "time" : 12:02:34    # should be type DateTime or Timestamp(<-- only SQL?)
}
```
| HTTP Code | Condition for return value
|:---       |:---
|201        |Order was placed, given an ID, has been dispatched to a vehicle and vehicle begins fulfillment
|400        |Customers input were not formatted properly (credit card number)
|404        |Resource not found

Example of `GET` with `/orders`
```HTTP
GET http://team22.supply.softwareengineeringii.com/orders/123
{
    vehicle json object
}
```