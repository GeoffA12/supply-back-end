import http.server
from http.server import BaseHTTPRequestHandler
import json
import mysql.connector as sqldb
import requests
from dispatch import Dispatch
from ENUMS.servicetype import type
from SERVER_UTILS.vehicle_utils import getRoute, getEta
# from serverutils import connectToSQLDB
from datetime import datetime
import time
import copy

def connectToSQLDB():
    return sqldb.connect(user='root', password='password', database='team22supply', port=6022)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.2'

    def getPOSTBody(self):
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        return json.loads(body)

    def getVehicles(self):
        vehicles = (
            (12345, 'Inactive', 'qw3256', 34, 'Toyota', 'V-9', 23.42, 42.12),
            (13579, 'Active', 'gf9012', 34, 'Mercedes', 'V-9', 102.43, 231.12),
            (12345, 'Active', 'qw3256', 34, 'Toyota', 'V-10', 12.51, 87.51),
            (12345, 'Maintenance', 'qw3256', 34, 'Toyota', 'V-8', 23.42, 124.31)
        )
        return vehicles
    def getOrder(self):
        order = {
            'orderID': 1234,
            'customerID': 42131,
            'serviceType': type.DRYCLEANING.value,
            'destination': "St. Edward's University",
            'timeOrderMade': '12:23:43',
        }
        return order

    # How to convert the body from a string to a dictionary
    # use 'loads' to convert from byte/string to a dictionary!
    def getPOSTBody(self):
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        return json.loads(body)

    def do_POST(self):
        path = self.path
        print(path)
        responseDict = {}
        if '/vehicleRequest' in path:
            sqlConnection = connectToSQLDB()
            # order = self.getPOSTBody()

            order = self.getOrder()
            # Until we get a vehicle DB, just this for now. But this would otherwise
            # Pull vehicle data from the vehicle table and choose one.
            # And of course as progress, we will add mor elogic to the
            # decision process of which vehicle is selected
            '''
            sqlConnection = connectToSQLDB()
            vehicleCursor = sqlConnection.cursor()
            '''
            '''
            # Query all vehicles whose status is 'Active'
            vehicleCursor.execute('SELECT * FROM vehicles, fleets 
                                WHERE status = Active
                                and type = drycleaning
                                and vehicles.fleetid and fleets.fleetid')
            vehicleEntries = vehicleCursor.fetchAll();  
            '''

            vehicles = self.getVehicles()

            filteredVehicles = list(filter(lambda x: x[1] == 'Active', vehicles))
            print(filteredVehicles)
            vehicle = filteredVehicles[0]

            # Capture vehicle tuple into its separate variables
            vid, status, liscensePlate, fleetId, make, model, vLon, vLat = vehicle

            # Seeing if the unpacking worked d:
            print(vehicle)
            print(vid)
            print(status)
            print(liscensePlate)
            print(fleetId)
            print(make)
            print(model)
            print(vLon)
            print(vLat)

            vehicleDict = {
                'vid': vid,
                'liscensePlate': liscensePlate,
                'make': make,
                'model': model,
                'curLocation': {
                    'lon': vLon,
                    'lat': vLat
                },
            }

            print(vehicleDict)
            # Deep copy the dictionary because we'll need to mutate what's in here a bit. Also separates this from the already
            # existing containers floating around
            dispatchDict = copy.deepcopy(order);
            dispatchDict['vid'] = vid

            ''' I think :C
            SELECT * from Vehicle, Fleet WHERE
            status = Available
            and serviceType = some serviceType
            and Vehicle.fleetId = Fleet.fleetId
            '''

            # Turn a destination dictionary into a tupled pair
            attrToTuple = dispatchDict.pop('destination');
            print(attrToTuple)

            # Here we would translate human readable to geo code, but for now we'll hardcode some points

            attrToTuple = {
                'lon' : 123.12,
                'lat' : 32.1
            }

            dispatchDict['loc_f'] = (attrToTuple['lon'], attrToTuple['lat'])
            dispatchDict['loc_0'] = (vLon, vLat)

            print(dispatchDict)

            dispatch = Dispatch(**dispatchDict)

            print(dispatch)

            print('Time: ', dispatch.timeCreated)
            # print(type(dispatch.timeCreated))

            timestamp = datetime.now().strftime('%H:%M:%S')

            print(dispatch.vid)

            insert = 'INSERT INTO dispatch (vid, custid, orderid, start_lat, start_lon, end_lat, end_lon, start_time, status, type) VALUES (%s %s %s %s %s %s %s %s %s %s)'% \
            (dispatch.vid, dispatch.cid, dispatch.oid, dispatch.loc_0[1], dispatch.loc_0[0], dispatch.loc_f[1], dispatch.loc_f[0], timestamp, dispatch.status, dispatch.sType)

            print(insert)

#            dispatchCursor = sqlConnection.cursor()
#            dispatchCursor.execute(insert)
#            sqlConnection.commit()

            eta = getEta()
            print(eta)

            vehicleDict['ETAInfo'] = {
                "Units": "HH:MM:SS",
                "ETA": eta
            }
            responseDict['vehicle'] = vehicleDict
            status = 200

        elif '/loginHandler' in path:
            dictionary = self.getPOSTBody()
            # To access a specific key from the dictionary:
            print(dictionary)
            username = dictionary['username']
            password = dictionary['password']

            sqlConnection = connectToSQLDB()
            cursor = sqlConnection.cursor()
            cursor.execute('SELECT username, password FROM fleetmanagers')
            rows = cursor.fetchall()
            usernameList = [x[0] for x in rows]
            passwordList = [x[1] for x in rows]

            # Make a dictionary from the usernameList and passwordList where the key:value pairs
            # are username:password
            userpass = dict(zip(usernameList, passwordList))

            if username in userpass and userpass[username] == password:
                status = 200

            # We'll send a 401 code back to the client if the user hasn't registered in our database
            else:
                status = 401

        # If we are receiving a request to register an account
        elif '/registerHandler' in path:
            dictionary = self.getPOSTBody()
            # To access a specific key from the dictionary:
            print(dictionary)
            username = dictionary['username']
            password = dictionary['password']
            email = dictionary['email']
            phone = dictionary['phoneNumber']

            sqlConnection = connectToSQLDB()
            cursor = sqlConnection.cursor()
            cursor.execute('SELECT username FROM fleetmanagers')
            rows = cursor.fetchall()
            usernameList = [x[0] for x in rows]

            # The equivalent of arr.contains(e)
            if username in usernameList:
                status = 401
            else:
                status = 200
                newCursor = sqlConnection.cursor()
                print(username)
                print(password)
                newCursor.execute('INSERT INTO fleetmanagers (username, password, email, phone) VALUES (%s, %s, %s, %s)',
                                  (username, password, email, phone))
                sqlConnection.commit()
                responseDict['Success'] = True

        else:
            status = 404

        self.send_response(status)
        self.end_headers()
        res = json.dumps(responseDict)
        bytesStr = res.encode('utf-8')
        self.wfile.write(bytesStr)

    def do_GET(self):
        vehicleList = self.getVehicles()
        path = self.path
        status = 200
        responseDict = {}
        if '/vehicleRequest' in path:
            responseDict = vehicleList

        elif '/etaRequest' in path:
            print()

        elif True:
            print()

        self.send_response(status)
        self.end_headers()
        res = json.dumps(responseDict)
        bytesStr = res.encode('utf-8')
        self.wfile.write(bytesStr)

def main():
    port = 4022
    # Create an http server using the class and port you defined
    httpServer = http.server.HTTPServer(('', port), SimpleHTTPRequestHandler)
    print("Running on port", port)
    # this next call is blocking! So consult with Devops Coordinator for
    # instructions on how to run without blocking other commands frombeing
    # executed in your terminal!
    httpServer.serve_forever()

if __name__ == '__main__':
    main()
