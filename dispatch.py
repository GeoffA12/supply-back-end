from datetime import datetime

class Dispatch(object):
    ver = '0.2'

    def __init__(self, **kwargs):
        self.sType = kwargs["serviceType"]
        self.vid = kwargs["vid"]
        self.cid = kwargs["customerID"]
        self.oid = kwargs["orderID"]
        self.loc_0 = kwargs["loc_0"]
        self.loc_f = kwargs["loc_f"]
        self.timeCreated = kwargs["timeOrderMade"]
        self.status = "In Progress"

    def getRoute(self, curLoc):
        print('my route')
        # do stuff to get the route

    def getETA(self, curLoc):
        print('my eta')
        # do stuff to get ETA, will probably need DateTime.now stuff

    def dispatchFulfilled(self):
        self.status = "Completed"

    def _asdict(self):
        return self.__dict__

    def __repr__(self):
        return f'Dispatch(' \
               f'{self.sType}, {self.vid}, {self.cid}, {self.oid}, {self.loc_0}, {self.loc_f}, {self.timeCreated}' \
               f', {self.isDone})'

    def __str__(self):
        return f'''Service Type: {self.sType}
Vehicle ID: {self.vid}
Customer ID: {self.cid}
Order ID: {self.oid}
Start Location: {self.loc_0}
End Location: {self.loc_f}
Time Order was Placed: {self.timeCreated},
Dispatch Status: {self.status}
'''

if __name__ == '__main__':
    Dispatch()