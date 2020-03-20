from datetime import datetime
from utils.serverutils import connectToSQLDB
from enums.dispatchstatus import DispatchStatus
from enums.servicetype import ServiceType


class Dispatch(object):
    ver = '0.5.0'
    
    def __init__(self, serviceType, vid, custid, orderid, loc_0, loc_f, timeOrderMade,
                 status=DispatchStatus.QUEUED):
        assert type(serviceType) is ServiceType
        assert type(status) is DispatchStatus
        
        self._serviceType = serviceType
        self._vid = vid
        self._custid = custid
        self._orderid = orderid
        self._loc_0 = loc_0
        self._loc_f = loc_f
        self._timeCreated = timeOrderMade
        self._status = status
    
    @property
    def serviceType(self):
        return self._serviceType
    
    @property
    def vid(self):
        return self._vid
    
    @property
    def custid(self):
        return self._custid
    
    @property
    def orderid(self):
        return self._orderid
    
    @property
    def loc_0(self):
        return self._loc_0
    
    @property
    def loc_f(self):
        return self._loc_f
    
    @property
    def timeCreated(self):
        return self._timeCreated
    
    @property
    def status(self):
        return self._status
    
    def getRoute(self, curLoc):
        print('my route')
        # do stuff to get the route
    
    def getETA(self, curLoc):
        print('my eta')
        # do stuff to get ETA, will probably need DateTime.now stuff
    
    def completed(self):
        self._status = DispatchStatus.DONE
        sqlConnection = connectToSQLDB()
        statement = 'UPDATE dispatch SET status = 3 WHERE orderid = %s'
        cursor = sqlConnection.cursor()
        cursor.execute(statement, (self._orderid,))
        cursor.commit()
        cursor.close()
        sqlConnection.close()
        # Update in DB
    
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
