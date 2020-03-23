# from utils.serverutils import connectToSQLDB


class FleetManager(object):
    ver = '0.0.0'
    
    def __init__(self, username):
        self._username = username
        self._fmid, self._email = self.__getid()
        self._fleetids = self.__getfleetids()
    
    @property
    def username(self):
        return self._username
    
    @property
    def fmid(self):
        return self._fmid
    
    @property
    def fleetids(self):
        return self._fleetids
    
    @property
    def email(self):
        return self._email
    
    def __getid(self):
        # print(username)
        sample = (
            (123, 'user1', 'email1@gmail.com'),
            (234, 'user2', 'email2@gmail.com'),
            (345, 'user3', 'email3@gmail.com'),
            (456, 'user4', 'email4@gmail.com'),
            (567, 'user5', 'email5@gmail.com')
            )
        data = [(x[0], x[2],) for x in sample if self.username in x][0]
        print(data)
        # sqlConnection = connectToSQLDB()
        # statement = 'SELECT fmid, email FROM fleets WHERE username = %s'
        # cursor = sqlConnection.cursor()
        # cursor.execute(statement, self.username)
        # response = cursor.fetchall()
        # sqlConnection.close()
        return data
    
    def __getfleetids(self):
        sample = (
            (1, 'user1'),
            (2, 'user1'),
            (3, 'user2'),
            (4, 'user1')
            )
        fleetids = [x[0] for x in sample if x[1] == self.username]
        # sqlConnection = connectToSQLDB()
        # statement = 'SELECT fleetid FROM fleets WHERE fmid = %s'
        # cursor = sqlConnection.cursor()
        # cursor.execute(statement, self.fmid)
        # fleetids = cursor.fetchall()
        # sqlConnection.close()
        return fleetids
    
    def __repr__(self):
        return f'''{self.username}'''
    
    def __str__(self):
        return f'''Username: {self.username}
Fleet Manager ID: {self.fmid}
Fleet Manager Email: {self.email}
Associated Fleets' IDs: {self.fleetids}
'''
