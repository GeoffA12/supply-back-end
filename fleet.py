from utils.serverutils import connectToSQLDB
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
    
    # def getVehicles(self):
    #     print('get vehicles')
    #     sqlConnection = connectToSQLDB()
    #     statement = f'SELECT * FROM vehicles WHERE fleetid = {self.fleetid}'
    #     cursor = sqlConnection.curor()
    #     cursor.execute(statement)
    #     vehicleList = cursor.fetchall()
    #     sqlConnection.close()
    #     return dict(enumerate(x for x in vehicleList))
    
    def asdict(self):
        return self.__dict__
    
    def __repr__(self):
        return f'''{self.fleetid}, {self.fmid}, {self.region}, {self.serviceType}'''
    
    def __str__(self):
        return f'''Fleet ID: {self.fleetid}
Fleet Manager: {self.fleetid}
Region Coverage: {self.region}
Service Type: {self.serviceType}'''
