import http.server
from http.server import BaseHTTPRequestHandler
import json
import mysql.connector as sqldb
import requests
from dispatch import Dispatch
from serverutils import connectToSQLDB
import datetime
import copy

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.2'

    def getVehicles(self):
        vehicles = (
            (12345, 'Inactive', 'qw3256', 34, ' Toyota', 'V-9', 23.42, 42.12,),
            (13579, 'Active', 'gf9012', 34, 'Mercedes', 'V-9', 102.43, 231.12,),
            (12345, 'Active', 'qw3256', 34, 'Toyota', 'V-10', 12.51, 87.51,),
            (12345, 'Maintenance', 'qw3256', 34, 'Toyota', 'V-8', 23.42, 124.31,)
        )
        return vehicles
    def getOrder(self):
        order = {
            'orderID': 1234,
            'customerID': 42131,
            'serviceType': 'DryCleaning',
            'destination': {
                'lon': 123.12,
                'lat': 51.12
            },
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
            vehicleCursor.execute('SELECT * FROM vehicles WHERE status = Active')
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
                'status': 'Active',
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

            # Turn a destination dictionary into a tupled pair
            attrToTuple = dispatchDict.pop('destination');
            print(attrToTuple)
            dispatchDict['loc_f'] = (attrToTuple['lon'], attrToTuple['lat'])
            dispatchDict['loc_0'] = (vLon, vLat)

            print(dispatchDict)

            dispatch = Dispatch(**dispatchDict)

            print(dispatch)

            status = 200

        else:
            status = 405

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
        if path.endswith('/vehicleRequest'):
            responseDict = vehicleList
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
