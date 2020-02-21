import http.server
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import mysql.connector as mariadb
import requests
from .dispatch import Dispatch
import datetime

def connectToMariaDB():
    return mariadb.connect(user='root', password='ShinyNatu34', database='team22demand')

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
                "status": "Delivering",
                "location": {
                    "lon": 23.42,
                    "lat": 42.12
                },
                "destination": {
                    "address1": "3001 S Congress Ave",
                    "address2": "St. Andres RM222D"
                }
            },
            {
                "vid": 98765,
                "serviceType": "DryCleaning",
                "vehicleMake": "Tesla",
                "liscencePlate": "TE1241",
                "status": "Delivered",
                "location": {
                    "lon": 45.12,
                    "lat": 10.31
                },
                "destination": {
                    "address1": "",
                    "address2": ""
                }
            }
        ]
        path = self.path
        responseDict = {}
        if path.endswith('/vehicleRequest'):
            dictionary = self.getPOSTBody()
            '''
            dictionary = {
                "serviceType" : "DryCleaning",  # Could probably be an ENUM
                "customerID" : 19821
                "orderID" : 123,
                "location" : {
                    "lon" : 45.12,
                    "lat" : 124.22
                },
                "timeOrderMade" : 12:02:34    # should be type DateTime
            }
            '''

            '''
            Until we get a vehicle DB, just this for now. But this would otherwise
            Pull vehicle data from the vehicle table and choose one.
            And of course as progress, we will add mor elogic to the
            decision process of which vehicle is selected
            '''

            mariadb_connection = connectToMariaDB()

            vehicle = vehicleList[1]
            '''
            Because we are receiving a payload that isn't formatted how we want it in our Dispatch, and maybe
            we can change what lives in dispatch, but for how it is, we need to break up our nesting
            and get it into tuple form. 
            '''
            attrToTuple = dictionary.pop("location")
            dictionary["loc_f"] = (attrToTuple["lon"], attrToTuple["lat"])

            dictionary["vid"] = vehicle["vid"]
            attrToTuple = vehicle.pop("location")
            dictionary["loc_0"] = (attrToTuple["lon"], attrToTuple["lat"])

            # Here, we're just converting the string of the time to the DateTime type.
            strToDateTime = datetime.strptime(dictionary["timeOrderMade"], '%H:%M:%S').time()
            dictionary["timeOrderMade"] = strToDateTime

            dispatch = Dispatch(**dictionary)

            responseDict = vehicle
            status = 200

        else:
            status = 404

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
                "status": "Delivering",
                "location": {
                    "lon": 23.42,
                    "lat": 42.12
                },
                "destination": {
                    "address1": "3001 S Congress Ave",
                    "address2": "St. Andres RM222D"
                }
            },
            {
                "vid": 98765,
                "serviceType": "DryCleaning",
                "vehicleMake": "Tesla",
                "liscencePlate": "TE1241",
                "status": "Delivered",
                "location": {
                    "lon": 45.12,
                    "lat": 10.31
                },
                "destination": {
                    "address1": "",
                    "address2": ""
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
    print('')

if __name__ == '__main__':
    main()