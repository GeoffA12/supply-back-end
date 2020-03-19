# from utils.serverutils import connectToSQLDB

class Fleet(object):
    ver = '0.1.1'
    
    def __init__(self, fleetid, fmid, region, serviceType):
        self.fleetid = fleetid
        self.fmid = fmid
        self.region = region
        self.serviceType = serviceType

    # def getVehicles(self):
    #     print('get vehicles')
    #     sqlConnection = connectToSQLDB()
    #     statement = f'SELECT * FROM vehicles WHERE fleetid = {self.fleetid}'
    #     with sqlConnection.curor() as cursor:
    #         cursor.execute(statement)
    #         vehicleList = cursor.fetchall()
    #         sqlConnection.close()
    #         return dict(enumerate(x for x in vehicleList))

    def asdict(self):
        return self.__dict__

    def __repr__(self):
        return f'''{self.fleetid}, {self.fmid}, {self.region}, {self.serviceType}'''

    def __str__(self):
        return f'''Fleet ID: {self.fleetid}
Fleet Manager: {self.fleetid}
Region Coverage: {self.region}
Service Type: {self.serviceType}'''
