import http.server
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import mysql.connector as sqldb
import requests
from .dispatch import Dispatch
from .serverutils import connectToSQLDB
import datetime

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.0'

    def getVehicles(self):
        vehicleList = [
            {
                "vid": 12345,
                "serviceType": "DryCleaning",
                "vehicleMake": "Toyota",
                "liscencePlate": "QW3456",
                "status": "Active",
                "location": {
                    "lon": 23.42,
                    "lat": 42.12
                },
                "destination": {
                    "lon": 125.12,
                    "lat": 213.21
                }
            },
            {
                "vid": 98765,
                "serviceType": "DryCleaning",
                "vehicleMake": "Tesla",
                "liscencePlate": "TE1241",
                "status": "Inactive",
                "location": {
                    "lon": 45.12,
                    "lat": 10.31
                },
                "destination": {
                    "lon": None,
                    "lat": None
                }
            }
        ]
        return vehicleList

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
            dictionary = self.getPOSTBody()

            # Until we get a vehicle DB, just this for now. But this would otherwise
            # Pull vehicle data from the vehicle table and choose one.
            # And of course as progress, we will add mor elogic to the
            # decision process of which vehicle is selected

            sqlConnection = connectToSQLDB()

            vehicle = self.getVehicles[1]
            vehicleCursor = sqlConnection.cursor()
            vehicleCursor.execute('SELECT * FROM vehicles WHERE status = Available')

            dictionary["vid"] = vehicle["vid"]

            attrToTuple = vehicle.pop("location")
            dictionary["loc_0"] = (attrToTuple["lon"], attrToTuple["lat"])

            attrToTuple = dictionary.pop("location")

            # lonlatDest = do something with map service to determine lon lat version of user human readable,
            # or maybe this happens on supply end

            dictionary["loc_f"] = (attrToTuple["lon"], attrToTuple["lat"])

            strToDateTime = datetime.strptime(dictionary["timeOrderMade"], '%H:%M:%S').time()
            dictionary["timeOrderMade"] = strToDateTime

            dispatch = Dispatch(**dictionary)

            vehicle["destination"]["lon"] = 231.12
            vehicle["destination"]["lat"] = 1.21
            responseDict = vehicle
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
