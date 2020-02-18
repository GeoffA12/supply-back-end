# Vehicle Request API
'''
From demand side, expecting incoming request with JSON object entailing order details
What the json object might look like
order = {
    "serviceType" : "dryCleaning",  # Could probably be an ENUM
    "customerID" : "12345",
    "address1" : "3001 S Congress Ave",
    "address2" : "St. Andres 222D",
    "phoneNum" : 9728002591
    "paymentMethod" : {
        "paymentType" : BOA,
        "name" : " Jeffrey Kacey Ng",
        "creditCardNum" : 1234123412341234,
        "CVV" : 123,
        "exp" : 01/21    # don't know if python Date can do just MM/YY, so might just be String
    }
    "time" : 12:02:34    # should be type DateTime or Timestamp(<-- only SQL?)
}

Q1: Given that this API will be receiving the order.json, will it also be responsible for writing it to the demandDB?
Probably??



'''

'''
Resources
Customer submits an order
POST http://team22.supply.softwareengineeringii.com/orders/1


'''

class VehicleRequestHandler():
    ver = '0.0'

    def post(self):
        '''
        Order gets written to the DemandDB

        Use order.json to create a Dispatch
        dispatch = Dispatch(necessary json object data unpacked)

        dispatch is written to SupplyDB

        Get all vehicle whose ETA to order.address1 is within acceptable discrepancy and contain serviceType
        Dispatch gets added to chosen vehicle's dispatch queue

        '''

    def get(self):
        '''
        Fleet manager probably wants some sort of access to dispatches. Might not exist here but instead in
        specifically SupplyBE handler(s)

        '''