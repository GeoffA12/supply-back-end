from datetime import datetime

from enums.dispatchstatus import DispatchStatus
from enums.servicetype import ServiceType


class Dispatch(object):
    ver = '0.5.0'

    def __init__(self, serviceType, vid, custid, orderid, loc_0, loc_f, timeOrderMade,
                 status = DispatchStatus.QUEUED):
        if type(serviceType) is not ServiceType:
            raise TypeError("Must use enum!")
    
        elif type(status) is not DispatchStatus:
            raise TypeError("Must use enum!")
    
        self.serviceType = serviceType
        self.vid = vid
        self.custid = custid
        self.orderid = orderid
        self.loc_0 = loc_0
        self.loc_f = loc_f
        self.timeCreated = timeOrderMade
        self.status = status
    
    def getRoute(self, curLoc):
        print('my route')
        # do stuff to get the route
    
    def getETA(self, curLoc):
        print('my eta')
        # do stuff to get ETA, will probably need DateTime.now stuff
    
    def asdict(self):
        return self.__dict__
    
    def __repr__(self):
        return f'Dispatch(' \
               f'{self.serviceType}, {self.vid}, {self.custid}, {self.orderid}, ' \
               f'{self.loc_0}, {self.loc_f}, {self.timeCreated}'
    
    def __str__(self):
        return f'''Service Type: {self.serviceType}
Vehicle ID: {self.vid}
Customer ID: {self.custid}
Order ID: {self.orderid}
Start Location: {self.loc_0}
End Location: {self.loc_f}
Time Order was Placed: {self.timeCreated},
Dispatch Status: {self.status}'''
