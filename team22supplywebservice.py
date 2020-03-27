
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


# def connectToSQLDB():
#     return sqldb.connect(user = 'root', password = 'password', database = 'team22supply', port = 6022)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.4.1'
    
    # How to convert the body from a string to a dictionary
    # use 'loads' to convert from byte/string to a dictionary!
    def getPOSTBody(self):
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        return json.loads(body)

    '''
    data I want or am expecting
    dictionary = {
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

        dictionary = self.getPOSTBody()
        sqlConnection = connectToSQLDB()
        cursor = sqlConnection.cursor()
        responseBody = {}

        # TODO: needs to be formatted
        if '/vehicleRequest' in path:
            print(dictionary)
            # Query all vehicles whose status is 'Active' and are a part of the fleet whose service time is the
            # incoming order's service type
            dictionary['serviceType'] = ServiceType.translate(dictionary['serviceType'])
            print(dictionary['serviceType'])
            data = [1, dictionary['serviceType'].value, ]
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
            dispatchDict = deepcopy(dictionary)
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
            print(dictionary)
            fleetToAddTo = dictionary.pop('fleetNum')
            print(dictionary)

            data = []
            for key, value in dictionary.items():
                print(key)
                entry = (1, value['LicensePlate'], int(fleetToAddTo), value['Make'], value['Model'], 12.12, 34.34)
                print(entry)
                data.append(entry)
            print(data)
            statement = '''INSERT INTO vehicles
                        (status, licenseplate, fleetid,
                        make, model, current_lat, current_lon)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            cursor.executemany(statement, data)
            sqlConnection.commit()

        elif '/removeVehicle' in path:
            status = 200
            # print(dictionary)
            del dictionary['fleetNum']
            print(dictionary)
    
            statement = 'DELETE FROM vehicles WHERE vid = %s'
            data = [(x,) for x in dictionary.values()]
            print(data)
            cursor.executemany(statement, data)
            sqlConnection.commit()
            
        elif '/addFleet' in path:
            status = 200
            print(dictionary)
    
            emailOrUser = dictionary['username']
            region = dictionary['region']
            serviceType = dictionary['serviceType']
    
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
    
        hasParams = '?' in path
        if hasParams:
            paramsOnlyString = path.split('/')[-1].strip('?')
            print(paramsOnlyString)
            paramsAsArray = paramsOnlyString.split('&')
            paramKeys = [x.split('=')[0] for x in paramsAsArray]
            print(paramKeys)
            if len(paramKeys) != len(set(paramKeys)):
                raise ValueError("You cannot parameterise duplicate parameters!")
            paramVals = [x.split('=')[1] for x in paramsAsArray]
            paramDict = dict(zip(paramKeys, paramVals))
    
        sqlConnection = connectToSQLDB()
        cursor = sqlConnection.cursor()
        responseBody = {}
    
        if '/vehicleRequest' in path:
            statement = 'SELECT * FROM vehicles'
            cursor.execute(statement)
            rows = cursor.fetchall()
            vehicles = [list(x) for x in rows]
            # print(vehicles)
            if hasParams:
                # Parameter for fleet master
                if 'user' in paramKeys:
                    user = paramDict['user']
                    print(user)
                    statement = '''SELECT vehicles.fleetid
                                FROM vehicles, fleets, fleetmanagers
                                WHERE vehicles.fleetid = fleets.fleetid
                                AND fleetmanagers.username = %s'''
                    cursor.execute(statement, (user,))
                    fleetIDs = cursor.fetchall()
                    if fleetIDs is None:
                        statement = '''SELECT vehicles.fleetid
                                    FROM vehicles, fleets, fleetmanagers
                                    WHERE vehicles.fleetid = fleets.fleetid
                                    AND fleetmanagers.email = %s'''
                        cursor.execute(statement, (user,))
                        fleetIDs = cursor.fetchall()
                    # print(ids)
                    fleetIDSet = set([x[0] for x in fleetIDs])
                    print(fleetIDSet)
                    # Filtering out all the vehicles whose fleetids are not associated to our fleet master
                    vehicles = [vehicle for fleetID in fleetIDSet for vehicle in rows if fleetID in vehicle]
        
                # Parameter for order id
                elif 'oid' in paramKeys:
<<<<<<< HEAD
                    oid = (paramDict['oid'],)
                    print(oid)
=======
                    oid = paramDict['oid']
>>>>>>> c827a3772ba3ebf996b11a93e8c5b182386e7b68
                    statement = '''SELECT vehicles.*
                                FROM dispatch, vehicles
                                WHERE vehicles.vid = dispatch.vid
                                AND orderid = %s'''
<<<<<<< HEAD
                    cursor = sqlConnection.cursor()
                    cursor.execute(statement, oid)
                    vehicles = cursor.fetchall()
                    print(vehicles)
                    cursor.close()

=======
                    cursor.execute(statement, (oid,))
                    vehicles = cursor.fetchone()
            
>>>>>>> c827a3772ba3ebf996b11a93e8c5b182386e7b68
                # Parameter for vehicle id
                elif 'vid' in paramKeys:
                    vid = int(paramDict['vid'])
                    vehicles = [x for x in rows if vid in x]
        
            vehicleColsNames = ['vehicleid', 'status', 'licenseplate', 'fleetid', 'make', 'model',
                                'current_lat', 'current_lon', 'last_heartbeat', 'date_added']
        
            vehiclesDictList = []
            for vehicle in vehicles:
                vehicleDict = {}
                for colName, colVal in zip(vehicleColsNames, vehicle):
                    if colName == 'current_lat' or colName == 'current_lon':
                        colVal = float(colVal)
                    vehicleDict[colName] = colVal
                vehiclesDictList.append(vehicleDict)
        
            responseBody = vehicles
            print(responseBody)
            status = 200
            for vehicleDict in responseBody:
                for k, v in vehicleDict.items():
                    print(k, v)

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
            vid = (paramDict['vid'],)
            print(vid)
            statement = '''SELECT did, orderid, custid, end_lat, end_lon,
                        type, start_time, status
                        FROM dispatch WHERE vid = %s'''
            print(statement)
            cursor = sqlConnection.cursor()
            cursor.execute(statement, vid)
            dispatchTup = cursor.fetchall()
            cursor.close()
            print('tup:', dispatchTup)
            dispatchListCopy = [list(x) for x in dispatchTup]
            print('List: ', dispatchListCopy)


            latlons = [(x[3], x[4]) for x in dispatchListCopy]
            dispatchList = [x[0:3] + x[5:] for x in dispatchListCopy]

            # eventually, none will ne a function that takes in a lat lon tup and translate into address
            revGeos = [None for x in latlons]
            for dispatch, address in zip(dispatchList, revGeos):
                dispatch.insert(3, address)

            dispatchCols = ['orderid', 'customerid', 'destination', 'serviceType',
                           'timeOrderCreated', 'status']
            dids = [x[0] for x in dispatchList]
            attr = [x[1:] for x in dispatchList]

            dispatches = {}
            for did, attribute, in zip(dids, attr):
                key = f'DispatchID{did}'
                dispatches[key] = {}
                for col, e in zip(dispatchCols, attribute):
                    if col == 'timeOrderCreated':
                        e = e.isoformat().replace('T', ' ')
                    dispatches[key][col] = e

            responseBody = dispatches
            print(responseBody)
            status = 200
            for k, v in responseBody.items():
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
