from enums.servicetype import ServiceType


class Fleet(object):
    ver = '0.1.1'
    
    def __init__(self, fleetid, fmid, region, serviceType):
        assert type(serviceType) is ServiceType
        
        self._fleetid = fleetid
        self._fmid = fmid
        self._region = region
        self._serviceType = serviceType
    
    @property
    def fleetid(self):
        return self._fleetid
    
    @property
    def fmid(self):
        return self._fmid
    
    @property
    def region(self):
        return self._region
    
    @property
    def serviceType(self):
        return self._serviceType
    
    def asdict(self):
        return self.__dict__
    
    def __repr__(self):
        return f'''Fleet({self.fleetid}, {self.fmid}, {self.region}, {self.serviceType})'''
    
    def __str__(self):
        return f'''Fleet ID: {self.fleetid}
Fleet Manager: {self.fleetid}
Region Coverage: {self.region}
Service Type: {self.serviceType}'''
