import time
from datetime import datetime
import sys

from ENUMS.dispatchstatus import DispatchStatus


class Dispatch(object):
    ver = '0.5'
    
    def __init__(self, serviceType, vid, customerID, orderID, loc_0, loc_f, timeOrderMade):
        self.sType = serviceType
        self.vid = vid
        self.cid = customerID
        self.oid = orderID
        self.loc_0 = loc_0
        self.loc_f = loc_f
        self.timeCreated = datetime.strptime(timeOrderMade, '%H:%M:%S').time()
        self.status = DispatchStatus.QUEUED
    
    def getRoute(self, curLoc):
        print('my route')
        # do stuff to get the route
    
    def getETA(self, curLoc):
        print('my eta')
        # do stuff to get ETA, will probably need DateTime.now stuff
    
    def _asdict(self):
        return self.__dict__
    
    def __repr__(self):
        return f'Dispatch(' \
               f'{self.sType}, {self.vid}, {self.cid}, {self.oid}, ' \
               f'{self.loc_0}, {self.loc_f}, {self.timeCreated}'
    
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
