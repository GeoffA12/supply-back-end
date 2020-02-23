import http.server
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import mysql.connector as sqldb
import requests
# from dispatch import Dispatch
# import datetime

def connectToSQLDB():
    return sqldb.connect(user='root', password='password', database='team22demand', port=6022)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.0'

    # How to convert the body from a string to a dictionary
    # use 'loads' to convert from byte/string to a dictionary!
    def getPOSTBody(self):
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        return json.loads(body)

    def do_POST(self):
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
        path = self.path
        print(path)
        responseDict = {}
        if '/vehicleRequest' in path:
            # dictionary = self.getPOSTBody()

            # Until we get a vehicle DB, just this for now. But this would otherwise
            # Pull vehicle data from the vehicle table and choose one.
            # And of course as progress, we will add mor elogic to the
            # decision process of which vehicle is selected

            # sqlConnection = connectToSQLDB()

            vehicle = vehicleList[1]

            # attrToTuple = dictionary.pop("location")
            # dictionary["loc_f"] = (attrToTuple["lon"], attrToTuple["lat"])
            #
            # dictionary["vid"] = vehicle["vid"]
            # attrToTuple = vehicle.pop("location")
            # dictionary["loc_0"] = (attrToTuple["lon"], attrToTuple["lat"])

            # strToDateTime = datetime.strptime(dictionary["timeOrderMade"], '%H:%M:%S').time()
            # dictionary["timeOrderMade"] = strToDateTime

            # dispatch = Dispatch(**dictionary)

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
