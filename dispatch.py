from datetime import datetime

class Dispatch(object):
    ver = '0.0'

    def __init__(self, **kwargs):
        self.sType = kwargs["serviceType"]
        self.vid = kwargs["vid"]
        self.cid = kwargs["customerID"]
        self.oid = kwargs["orderID"]
        self.loc_0 = kwargs["loc_0"]
        self.loc_f = kwargs["loc_f"]
        self.timeCreated = kwargs["timeOrderMade"]
        self.isDone = False

    def getRoute(self, curLoc):
        print('my route')
        # do stuff to get the route

    def getETA(self, curLoc):
        print('my eta')
        # do stuff to get ETA, will probably need DateTime.now stuff

    def dispatchFulfilled(self):
        self.isDone = True

    def _asdict(self):
        return self.__dict__

    def __repr__(self):
        return f'Dispatch(' \
               f'{self.sType}, {self.vid}, {self.cid}, {self.oid}, {self.loc_0}, {self.loc_f}, {self.timeCreated},' \
               f' {self.isDone})'

    def __str__(self):
        return f'''Service Type: {self.sType}
Vehicle ID: {self.vid}
Customer ID: {self.cid}
Order ID: {self.oid}
Start Location: {self.loc_0}
End Location: {self.loc_f}
Time Order was Placed: {self.timeCreated}, 
Dispatch Fulfilled: {self.isDone}
'''

if __name__ == '__main__':
    v = {
            "vid": 98765,
            "serviceType": "DryCleaning",
            "vehicleMake": "Tesla",
            "liscencePlate": "TE1241",
            "status": "Delivered",
            "location": {
                "lon": 45.12,
                "lat": 10.31
            },
            "destination": {
                "address1": "",
                "address2": ""
            }
        }
    dictionary = {
            "serviceType" : "DryCleaning",
            "customerID" : 19821,
            "orderID" : 123,
            "location" : {
                "lon" : 45.12,
                "lat" : 124.22
            },
            "timeOrderMade" : "12:2:34"
        }
    attrToTuple = dictionary.pop("location")
    dictionary["loc_f"] = (attrToTuple["lon"], attrToTuple["lat"])

    dictionary["vid"] = v["vid"]
    attrToTuple = v.pop("location")
    dictionary["loc_0"] = (attrToTuple["lon"], attrToTuple["lat"])

    strToDateTime = datetime.strptime(dictionary["timeOrderMade"], '%H:%M:%S').time()
    dictionary["timeOrderMade"] = strToDateTime

    dispatch1 = Dispatch(**dictionary)
    print(dispatch1)
    # for k, v in dispatch1._asdict().items():
    #     print(f'{k} --> {v}')

    dispatch1.dispatchFulfilled()
    print(dispatch1)

print(''' Dispatch Record SQL Table
 ___________________________________________________________________________________________________
| (PK) vid  | (PK) oid  | loc_0_lon | loc_0_lat | loc_f_lon | loc_f_lat | timeCreated   | isDone    |
| bigint    | bigint    | bigfloat  | bigfloat  | bigfloat  | bigfloat  | DateTime      | boolean   |
|:---       |:---       |:---       |:---       |:---       |:---       |:---           |:---       |
| 12345     | 123       | 23.42     | 42.12     | 45.12     | 124.22    | 05:18:21      | False     |
| 12345     | 5421      | 98.12     | 198.64    | 151.214   | 125.41    | 15:43:12      | True      |
| 45145     | 653124    | 214.12    | 56.01     | 141.121   | 215.231   | 23:51:59      | False     |
| 12345     | 41231     | 123.12    | 32.12     | 1.42      | 12.12     | 13:13:34      | False     |
| 31512     | 674134    | 71.13     | 52.53     | 89.121    | 53.13     | 10:42:31      | True      |
| 31512     | 41512     | 134.142   | 231.91    | 151.31    | 240.12    | 09:23:01      | True      |
| ...       | ...       | ...       | ...       | ...       | ...       | ...           | ...       |
|___________|___________|___________|___________|___________|___________|_______________|___________|

''')