
import http.server
from http.server import BaseHTTPRequestHandler
import json
import mysql.connector as sqldb
import requests
from dispatch import Dispatch
from enums.servicetype import ServiceType
from enums.vehiclestatus import VehicleStatus
from enums.dispatchstatus import DispatchStatus
from utils.vehicleutils import getRoute, getEta
from utils.serverutils import connectToSQLDB
from copy import deepcopy
# from datetime import datetime
import urllib.parse as urlparser
from urllib.parse import parse_qs

# def connectToSQLDB():
#     return sqldb.connect(user = 'root', password = 'password', database = 'team22supply', port = 6022)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.4.2'
    '''
    SendGrid API Key: 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
    '''
    
    # How to convert the body from a string to a dictionary
    # use 'loads' to convert from byte/string to a dictionary!
    def getPOSTBody(self):
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        return json.loads(body)
    
    '''
    data I want or am expecting
    postBody = {
            'serviceType': 'DRYCLEANING',
            'custid': 1234567,
            'orderid': 1234,
            'destination': {
                'lat': 123,
                'lon': 123
                },
            'timeOrderMade': '2018-03-29T13:34:00.000'
            }
    '''
    
    def do_POST(self):
        path = self.path
        print(path)
        status = 404

        postBody = self.getPOSTBody()
        sqlConnection = connectToSQLDB()
        cursor = sqlConnection.cursor()
        responseBody = {}

        # TODO: needs to be formatted
        if '/vehicleRequest' in path:
            print(postBody)
            # Query all vehicles whose status is 'Active' and are a part of the fleet whose service time is the
            # incoming order's service type
            postBody['serviceType'] = ServiceType.translate(postBody['serviceType'])
            print(postBody['serviceType'])
            data = [1, postBody['serviceType'].value, ]
            statement = '''SELECT vid, licenseplate,
                        make, model, current_lat, current_lon
                        FROM vehicles, fleets
                        WHERE vehicles.status = %s AND type = %s
                        AND vehicles.fleetid = fleets.fleetid'''
            cursor.execute(statement, tuple(data))
            vehicleEntries = cursor.fetchall()
            if vehicleEntries is None:
                data[0] = 2
                cursor.execute(statement, tuple(data))
                vehicleEntries = cursor.fetchall()
            
            print(vehicleEntries)
            allPostions = [(x[4], x[5]) for x in vehicleEntries]
            
            vehicle = vehicleEntries[0]
            
            # Capture vehicle tuple into its separate variables
            vid, licensePlate, make, model, vLat, vLon = vehicle
            
            # Seeing if the unpacking worked d:
            print(vehicle)
            
            print(vid)
            print(licensePlate)
            print(make)
            print(model)
            print(vLon)
            print(vLat)

            vLat = float(vLat)
            vLon = float(vLon)
            vehicleDict = {
                'vid': vid,
                'licensePlate': licensePlate,
                'make': make,
                'model': model,
                'curLocation': {
                    'lat': vLat,
                    'lon': vLon
                    },
                }
            
            print(vehicleDict)
            dispatchDict = deepcopy(postBody)
            dispatchDict['vid'] = vid
            
            # Turn a destination dictionary into a tupled pair
            destination = dispatchDict.pop('destination')
            
            dispatchDict['loc_f'] = (destination['lat'], destination['lon'])
            dispatchDict['loc_0'] = (vLat, vLon)
            
            print(dispatchDict)
            
            dispatch = Dispatch(**dispatchDict)
            
            print(dispatch)
            
            data = (
                dispatch.vid, dispatch.custid, dispatch.orderid,
                dispatch.loc_0[0], dispatch.loc_0[1], dispatch.loc_f[0], dispatch.loc_f[1],
                dispatch.timeCreated, dispatch.status.value, dispatch.serviceType.value,
                )
            statement = '''INSERT INTO dispatch
                        (vid, custid, orderid, start_lat, start_lon,
                        end_lat, end_lon, start_time, status, type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(statement, data)
            sqlConnection.commit()
            
            eta = getEta()[1]
            print(eta)
            
            vehicleDict['ETA'] = eta
    
            status = 200
            responseBody = vehicleDict
        
        elif '/addVehicle' in path:
            status = 200
            print(postBody)
            '''
            [{'fleetid': '8', 'make': 'Honda', 'model': 'Civic', 'licensePlate': 'AZ4915', 'dateAdded':
            '2020-03-28T08:34:32.698Z'}]
            '''
            data = []
            for vehicleDict in postBody:
                # This is Steds btw d: ==> 30.2264, 97.7553,
                entry = (2, vehicleDict['licensePlate'], vehicleDict['fleetid'],
                         vehicleDict['make'], vehicleDict['model'],
                         30.2264, 97.7553, vehicleDict['dateAdded'].replace('T', ' ').replace('Z', ' '))
                data.append(entry)
            print(data)
            statement = '''INSERT INTO vehicles
                        (status, licenseplate, fleetid,
                        make, model, current_lat, current_lon, date_added)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.executemany(statement, data)
            sqlConnection.commit()

        elif '/removeVehicle' in path:
            status = 200
            print(postBody)
            '''
            [{'vehicleid': '8'}, {'vehicleid': '4'}, {'vehicleid': '1'}, {'vehicleid': '6'},]
            '''
            data = [(vid,) for viddict in postBody for vid in viddict.values()]

            print(data)
            statement = 'DELETE FROM vehicles WHERE vid = %s'
            cursor.executemany(statement, data)
            sqlConnection.commit()

        elif '/updateVehicle' in path:
            print()
            '''
            Things that I will allow updating of the vehicle
            status
            licenseplate
            fleetid
            make (?)
            model (?)
            current_lat
            current_lon
            last_heartbeat
            
            Precondition(s):
            postBody must contain the key
            'vid' with a value of a vehicle that exists in the db
            and
            at least one more key named the same way as the above mentioned allowed update attributes
            Expected incoming format
            [{
                'vid': 1,
                'status': 1,
                }, {
                'vid': 4,
                'status': 2,
                }, {
                'vid': 2,
                'status': 1,
                'last_heartbeat': '12:41:13.513'
                }, ]
            '''

        elif '/addFleet' in path:
            status = 200
            print(postBody)
    
            emailOrUser = postBody['username']
            region = postBody['region']
            serviceType = postBody['serviceType']
    
            statement = 'SELECT fmid FROM fleetmanagers WHERE email = %s OR username = %s'
            data = (emailOrUser, emailOrUser,)
            cursor.execute(statement, data)
            fmid = cursor.fetchone()[0]
            data = (region, serviceType, fmid,)
            print(data)
            statement = 'INSERT INTO fleets (region, type, fmid) VALUES (%s, %s, %s)'
            cursor.execute(statement, data)
            sqlConnection.commit()
    
        cursor.close()
        sqlConnection.close()
        self.send_response(status)
        self.end_headers()
        res = json.dumps(responseBody)
        bytesStr = res.encode('utf-8')
        self.wfile.write(bytesStr)
    
    def do_GET(self):
        path = self.path
        print(path)
        status = 404
        parsedPath = urlparser.urlparse(path)
        print(parsedPath)
        paramsDict = parse_qs(parsedPath.query)
        print(paramsDict)
        hasParams = len(paramsDict) != 0
        print(hasParams)

        sqlConnection = connectToSQLDB()
        cursor = sqlConnection.cursor()
        responseBody = {}

        '''
        Vehicle Request Resource Handler
        As a generic GET request, our handler will return all vehicles that exists in our database formatted like so:
            [
                {
                    "vehicleid": 28,
                    "status": "active",
                    "licenseplate": "123456",
                    "fleetid": 5,
                    "make": "Toyota",
                    "model": "V-9",
                    "current_lat": 30.2264,
                    "current_lon": 97.7553,
                    "last_heartbeat": null,
                    "date_added": "2018-03-29T13:34:00"
                },
                {
                    "vehicleid": 30,
                    "status": "active",
                    "licenseplate": "VA4891",
                    "fleetid": 5,
                    "make": "Toyota",
                    "model": "V-9",
                    "current_lat": 30.2264,
                    "current_lon": 97.7553,
                    "last_heartbeat": null,
                    "date_added": "2018-03-29T00:00:00"
                }, .. , {n-th vehicle}
            ]
            
        The addition of parameters will be a filtering process
        '''
        if '/vehicleRequest' in path:
            statement = 'SELECT * FROM vehicles'
            cursor.execute(statement)
            rows = cursor.fetchall()
            vehicles = [list(x) for x in rows]
            fleetIDs = list(set([x[3] for x in vehicles]))
    
            # print(vehicles)
            if hasParams:
                # Parameter for fleet master
                if 'user' in paramsDict:
                    users = paramsDict['user']

                    usersCopy = deepcopy(users)
                    users = [(x, x) for x in usersCopy]
                    print(users)
                    statement = '''SELECT fleets.fleetid
                                FROM fleets, fleetmanagers
                                WHERE fleets.fmid = fleetmanagers.fmid
                                AND (fleetmanagers.username = %s
                                OR fleetmanagers.email = %s)'''
                    fleetIDs = []
                    for user in users:
                        cursor.execute(statement, user)
                        temp = cursor.fetchall()
                        flatten = [item for sublist in temp for item in sublist]
                        print(flatten)
                        fleetIDs.extend(flatten)
                        print(fleetIDs)
                    print(fleetIDs)
                    vehicles = [vehicle for fleetID in fleetIDs for vehicle in rows if fleetID == vehicle[3]]
        
                # Parameter for order id
                # TODO: need to conform to new method of parsing
                elif 'oid' in paramsDict:
                    oid = paramsDict['oid']
                    statement = '''SELECT vehicles.*
                                FROM dispatch, vehicles
                                WHERE vehicles.vid = dispatch.vid
                                AND orderid = %s'''

                    cursor.execute(statement, (oid,))
                    vehicles = cursor.fetchone()

                # Parameter for vehicle id
                elif 'vid' in paramsDict:
                    vids = set(paramsDict['vid'])
                    print(vids)
                    print(rows)
                    vehicles = [vehicle for vehicleID in vids for vehicle in rows if int(vehicleID) == vehicle[0]]
                    print(vehicles)

            print(fleetIDs)
            fleets = {
                'fleets': fleetIDs
                }
            print(fleets)

            vehicleColsNames = ['vehicleid', 'status', 'licenseplate', 'fleetid', 'make', 'model',
                                'current_lat', 'current_lon', 'last_heartbeat', 'date_added']

            vehiclesDictList = [fleets]
            print(vehiclesDictList)
            for vehicle in vehicles:
                vehicleDict = {}
                for colName, colVal in zip(vehicleColsNames, vehicle):
                    if colName == 'current_lat' or colName == 'current_lon':
                        colVal = float(colVal)
                    elif colName == 'date_added':
                        colVal = colVal.isoformat()
                    vehicleDict[colName] = colVal
                vehiclesDictList.append(vehicleDict)

            responseBody = vehiclesDictList
            print(responseBody)
            status = 200
            # for vehicleDict in responseBody:
            #     for k, v in vehicleDict.items():
            #         print(k, v)

        # TODO: Not sure if it works
        elif '/etaRequest' in path:
            # can ask about eta based on vid and oid
            # cannot ask with no parameters
            statement = '''SELECT type, vid, custid, orderid,
                        start_lat, start_lon, end_lat, end_lon,
                        start_time, status
                        FROM dispatch WHERE '''
            if 'vid' in paramKeys:
                data = (int(paramDict['vid']),)
                statement += 'vid = %s'

            elif 'oid' in paramKeys:
                data = (int(paramDict['oid']),)
                statement += 'orderid = %s'

            cursor = sqlConnection.cursor()
            cursor.execute(statement, data)
            dispatchTup = cursor.fetchone()[0]
            cursor.close()
        
            serviceType, vid, custid, orderid, \
            start_lat, start_lon, end_lat, end_lon, \
            start_time, status = dispatchTup
        
            dispatchDict = {
                'serviceType': serviceType,
                'vid': vid,
                'custid': custid,
                'orderid': orderid,
                'loc_0': (start_lat, start_lon),
                'loc_f': (end_lat, end_lon),
                'timeOrderMade': start_time,
                'status': DispatchStatus.translate(status)
                }
        
            dispatch = Dispatch(**dispatchDict)
        
            statement = 'SELECT current_lat, current_lon FROM vehicles WHERE vid = %s'
            cursor = sqlConnection.cursor()
            cursor.execute(statement)
            curPos = cursor.fetchone()[0]
            cursor.close()
            eta = dispatch.getETA(curPos)

            responseBody = {
                'ETA': eta
                }
            print(responseBody)
            status = 200

        # TODO: Need to change response body
        elif '/getDispatch' in path:
            vids = paramsDict['vid']
            print(vids)

            vidsCopy = deepcopy(vids)
            vids = [(x,) for x in vidsCopy]
            print(vids)
            statement = '''SELECT * FROM dispatch WHERE vid = %s'''
            print(statement)
            dispatches = []
            for vid in vids:
                cursor = sqlConnection.cursor()
                cursor.execute(statement, vid)
                dispatchTup = cursor.fetchall()
                # print('tup:', dispatchTup)
                dispatches.extend(list(dispatchTup))

            print(dispatches)
            dispatchesCopy = deepcopy(dispatches)

            dispatches = []
            for dispatch in dispatchesCopy:
                startLat, startLon = dispatch.pop(4), dispatch.pop(5)
                startHuman = 'St. Edward\'s University'
                startDict = {
                    'humanReadable': startHuman,
                    'lat': float(startLat),
                    'lon': float(startLon)
                    }
    
                endLat, endLon = dispatch.pop(6), dispatch.pop(7)
                endHuman = '1234 That Street Ave'
                endDict = {
                    'humanReadable': endHuman,
                    'lat': float(endLat),
                    'lon': float(endLon)
                    }
                dispatch.insert(4, startDict)
                dispatch.insert(5, endDict)
                dispatches.append(dispatch)

            print(dispatches)

            dispatchColsNames = ['did', 'vid', 'custid', 'orderid',
                                 'startLocation', 'endLocation',
                                 'start_time', 'status', 'serviceType']

            dispatchDictList = []
            for dispatch in dispatches:
                dispatchDict = {}
                for colName, colVal in zip(dispatchColsNames, dispatch):
                    if colName == 'start_time':
                        colVal = colVal.isoformat()
                    dispatchDict[colName] = colVal
                dispatchDictList.append(dispatchDict)

            responseBody = dispatchDictList
            # print(responseBody)
            status = 200
            for dispatch in responseBody:
                for k, v in dispatch.items():
                    print(k, v)

        cursor.close()
        sqlConnection.close()
        self.send_response(status)
        self.end_headers()
        res = json.dumps(responseBody)
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
