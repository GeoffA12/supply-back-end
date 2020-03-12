import http.server
from http.server import BaseHTTPRequestHandler
import json
import mysql.connector as sqldb
import requests
from dispatch import Dispatch
from ENUMS.servicetype import ServiceType
from ENUMS.vehiclestatus import VechileStatus
from ENUMS.dispatchstatus import DispatchStatus
from SERVER_UTILS.vehicle_utils import getRoute, getEta
# from serverutils import connectToSQLDB
from datetime import datetime
import time
import copy
import random


def connectToSQLDB():
    return sqldb.connect(user = 'root', password = 'password', database = 'team22supply', port = 6022)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.3.1'
    
    def getVehicles(self):
        vehicles = (
            (12345, 'Inactive', 'qw3256', 34, 'Toyota', 'V-9', 23.42, 42.12),
            (13579, 'Active', 'gf9012', 34, 'Mercedes', 'V-9', 102.43, 22.22),
            (12345, 'Active', 'qw3256', 34, 'Toyota', 'V-10', 12.51, 87.51),
            (12345, 'Maintenance', 'qw3256', 34, 'Toyota', 'V-8', 23.42, 124.31)
            )
        return vehicles
    
    def getOrder(self):
        order = {
            'orderID': random.random(),
            'customerID': 42131,
            'serviceType': ServiceType.DRYCLEANING.value,
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
        dictionary = self.getPOSTBody()

        if '/vehicleRequest' in path:
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
                                WHERE status = 1
                                and type = 1
                                and vehicles.fleetid = fleets.fleetid')
            vehicleEntries = vehicleCursor.fetchAll();
            '''
    
            vehicles = self.getVehicles()
    
            filteredVehicles = list(filter(lambda x: x[1] == 'Active', vehicles))
            print(filteredVehicles)
            vehicle = filteredVehicles[0]
    
            # Capture vehicle tuple into its separate variables
            vid, status, licensePlate, fleetId, make, model, vLon, vLat = vehicle
    
            # Seeing if the unpacking worked d:
            print(vehicle)
            print(vid)
            print(status)
            print(licensePlate)
            print(fleetId)
            print(make)
            print(model)
            print(vLon)
            print(vLat)
    
            vehicleDict = {
                'vid': vid,
                'liscensePlate': licensePlate,
                'make': make,
                'model': model,
                'curLocation': {
                    'lon': vLon,
                    'lat': vLat
                    },
                }
    
            print(vehicleDict)
            # Deep copy the dictionary because we'll need to mutate what's in here a bit. Also separates this from
            # the already
            # existing containers floating around
            dispatchDict = copy.deepcopy(order)
            dispatchDict['vid'] = vid
    
            # Turn a destination dictionary into a tupled pair
            attrToTuple = dispatchDict.pop('destination')
            print(attrToTuple)
    
            # Here we would translate human readable to geo code, but for now we'll hardcode some points
    
            attrToTuple = {
                'lon': 123.12,
                'lat': 32.1
                }
    
            dispatchDict['loc_f'] = (attrToTuple['lon'], attrToTuple['lat'])
            dispatchDict['loc_0'] = (vLon, vLat)
    
            print(dispatchDict)
    
            dispatch = Dispatch(**dispatchDict)
    
            print(dispatch)
    
            print('Time: ', dispatch.timeCreated)
            # print(type(dispatch.timeCreated))
    
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
            print(dispatch.vid)
    
            statement = '''INSERT INTO dispatch
                            (vid, custid, orderid, start_lat, start_lon, end_lat, end_lon, start_time, status, type)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            data = (dispatch.vid, dispatch.cid, dispatch.oid,
                    dispatch.loc_0[1], dispatch.loc_0[0], dispatch.loc_f[1], dispatch.loc_f[0],
                    timestamp, dispatch.status.value, dispatch.sType
                    )
            sqlConnection = connectToSQLDB()
            with sqlConnection.cursor() as cursor:
                cursor.execute(statement, data)
                sqlConnection.commit()
                sqlConnection.close()
    
            eta = getEta()[1]
            print(eta)
    
            vehicleDict['ETA'] = eta
    
            status = 200
            responseDict = vehicleDict
        
        elif '/addVehicle' in path:
            print(dictionary)
            fleetToAddTo = dictionary.pop('fleetNum')
            print(dictionary)

            vehicleEntries = []
            
            for key, value in dictionary.items():
                print(key)
                data = (1, value['Liscence Plate'], int(fleetToAddTo), value['Make'], value['Model'], 12.12, 34.34)
                print(data)
                vehicleEntries.append(data)
            print(vehicleEntries)
            print(data)

            statement = '''INSERT INTO vehicles
                            (status, licenseplate, fleetid, make, model, current_lat, current_lon)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            sqlConnection = connectToSQLDB()
            with sqlConnection.cursor() as cursor:
                cursor.execute(statement, data)
                sqlConnection.commit()
                sqlConnection.close()

            status = 200
            responseDict = dictionary

        elif '/removeVehicle' in path:
            print(dictionary)
            fleetToAddTo = dictionary.pop('fleetNum')
            print(dictionary)

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
