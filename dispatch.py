from enums.dispatchstatus import DispatchStatus
from enums.servicetype import ServiceType
from utils.mappingutils import getETA, getRoute


class Dispatch(object):
    ver = '0.5.1'

    def __init__(self, serviceType, vid, custid, orderid, loc_0, loc_f, timeOrderMade, status=DispatchStatus.RUNNING):
        assert type(serviceType) is ServiceType
        assert type(status) is DispatchStatus
        # print(timeOrderMade)
        self._serviceType = serviceType
        self._vid = vid
        self._custid = custid
        self._orderid = orderid
        self._loc_0 = loc_0
        self._loc_f = loc_f
        self._timeCreated = timeOrderMade
        self._status = status
        self._route = self.getRoute(loc_0)

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

    @property
    def route(self):
        return self._route

    # TODO Update coverage run
    def getRoute(self, curPos):
        startLat, startLon = curPos
        print(curPos)
        print(startLat)
        print(startLon)
        print(self._loc_f)
        route = getRoute(startLat=startLat,
                startLon=startLon,
                endLat=self._loc_f[0],
                endLon=self._loc_f[1])
        return route

    def getETA(self, curPos):
        startLat, startLon = curPos
        eta = getETA(startLat=startLat,
                startLon=startLon,
                endLat=self._loc_f[0],
                endLon=self._loc_f[1])
        return eta

    def completed(self):
        self._status = DispatchStatus.DONE

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
Dispatch Status: {self.status}
Route: {self._route}'''
