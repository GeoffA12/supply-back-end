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
    ver = '0.4.0'
    
    # How to convert the body from a string to a dictionary
    # use 'loads' to convert from byte/string to a dictionary!
    def getPOSTBody(self):
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        return json.loads(body)

    '''
    data I want or am expecting
    dictionary = {
            'serviceType': ServiceType.DRY_CLEANING,
            'custid': 1234567,
            'orderid': 1234,
            'destination': {
                'lat': 123,
                'lon': 123
                },
            'timeOrderMade': datetime(2011, 11, 4, 0, 5, 23)
            }
    '''
    
    def do_POST(self):
        path = self.path
        print(path)
        responseDict = {}
        dictionary = self.getPOSTBody()
        sqlConnection = connectToSQLDB()
        
        if '/vehicleRequest' in path:
            print(dictionary)
            # Query all vehicles whose status is 'Active' and are a part of the fleet whose service time is the
            # incoming order's service type
            data = [1, dictionary['serviceType'], ]
            statement = '''SELECT vid, licenseplate,
                        make, model, current_lat, current_lon
                        FROM vehicles, fleets
                        WHERE vehicles.status = %s AND type = %s
                        AND vehicles.fleetid = fleets.fleetid'''
            cursor = sqlConnection.cursor()
            cursor.execute(statement, tuple(data))
            vehicleEntries = cursor.fetchall()
            if vehicleEntries is None:
                data[0] = 2
                cursor = sqlConnection.cursor()
                cursor.execute(statement, tuple(data))
                vehicleEntries = cursor.fetchall()
            
            cursor.close()
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
                dispatch.timeCreated, dispatch.status.value, dispatch.serviceType.value
                )
            statement = '''INSERT INTO dispatch
                        (vid, custid, orderid, start_lat, start_lon,
                        end_lat, end_lon, start_time, status, type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor = connectToSQLDB.cursor()
            cursor.execute(statement, data)
            sqlConnection.commit()
            cursor.close()
            
            eta = getEta()[1]
            print(eta)
            
            vehicleDict['ETA'] = eta
            
            status = 200
            responseDict = vehicleDict
        
        elif '/addVehicle' in path:
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
            cursor = sqlConnection.cursor()
            cursor.executemany(statement, data)
            sqlConnection.commit()
            cursor.close()

            status = 200
        
        elif '/removeVehicle' in path:
            print(dictionary)
            
            statement = 'DELETE FROM vehicles (vid) WHERE vid = %s'
            data = ((x,) for x in dictionary['deleteMe'])
            cursor = sqlConnection.cursor()
            cursor.executemany(statement, data)
            sqlConnection.commit()
            cursor.close()
            
            status = 200
        
        elif '/addFleet' in path:
            print(dictionary)
            dictionary = {
                'newFleet1': {
                    'region': 'Austin',
                    'serviceType': 'Dry Cleaning',
                    'fmid': 123
                    }
                }
            data = []
            for key, value in dictionary.items():
                print(key)
                entry = (value['region'], value['serviceType'], value['fmid'])
                print(entry)
                data.append(entry)
            print(data)
            statement = 'INSERT INTO fleets (region, type, fmid) VALUES (%s, %s, %s)'
            cursor = sqlConnection.cursor()
            cursor.execute(statement, data)
            sqlConnection.commit()
            cursor.close()

            status = 200
        
        else:
            status = 404
        
        sqlConnection.close()
        self.send_response(status)
        self.end_headers()
        res = json.dumps(responseDict)
        bytesStr = res.encode('utf-8')
        self.wfile.write(bytesStr)
    
    def do_GET(self):
        # vehicleList = self.getVehicles()
        path = self.path
        print(path)
        paramsOnlyString = path.split('/')[-1].strip('?')
        print(paramsOnlyString)
        paramsAsArray = paramsOnlyString.split('&')
    
        paramKeys = [x.split('=')[0] for x in paramsAsArray]
        if len(paramKeys) != len(set(paramKeys)):
            raise ValueError("You cannot parameterise duplicate parameters!")
        paramVals = [x.split('=')[1] for x in paramsAsArray]
        paramDict = dict(zip(paramKeys, paramVals))

        sqlConnection = connectToSQLDB()
        responseDict = {}
    
        if '/vehicleRequest' in path:
            # can make a get request for vehicles based on fmuser, oid, vid
            statement = 'SELECT * FROM vehicles'
            cursor = sqlConnection.cursor()
            cursor.execute(statement)
            rows = cursor.fetchall()
            cursor.close()
            vehicles = [x for x in rows]
        
            # Parameter for fleet master
            if 'user' in paramKeys:
                user = (paramDict['user'],)
                statement = '''SELECT vehicles.fleetid
                            FROM vehicles, fleets, fleetmanagers
                            WHERE vehicles.fleetid = fleets.fleetid
                            AND fleetmanagers.username = %s'''
                cursor = sqlConnection.cursor()
                cursor.execute(statement, user)
                fleetIDs = cursor.fetchall()

                # Filtering out all the vehicles whose fleetids are not associated to our fleet master
                vehicles = [vehicle for ids in fleetIDs for vehicle in rows if ids in rows]

                # # Formatting for JS data parsing
                # vehicles = [[row[3], row[0], f'{row[5]}: {row[6]}',
                #              f'Lat: {float(row[6])} Lon: {float(row[7])}',
                #              row[1], row[2], row[8]
                #              ] for row in filtered]
        
            # Parameter for order id
            elif 'oid' in paramKeys:
                oid = (paramDict['oid'])
                statement = '''SELECT vehicles.*
                            FROM dispatch, vehicles
                            WHERE vehicles.vid = dispatch.vid
                            AND oid = %s'''
                cursor = sqlConnection.cursor()
                cursor.execute(statement, oid)
                vehicles = cursor.fetchone()
                cursor.close()

            # Parameter for vehicle id
            elif 'vid' in paramKeys:
                vid = int(paramDict['vid'])
                vehicles = [x for x in rows if vid in x]

            vehicleCols = ['status', 'licenseplate', 'fleetid', 'make', 'model',
                           'current_lat', 'current_lon', 'last_heartbeat']
            vids = [x[0] for x in vehicles]
            attr = [x[1:] for x in vehicles]

            vehicles = {}
            for vid in vids:
                key = f'VehicleID{vid}'
                vehicles[key] = {}
                for a in attr:
                    for col, e in zip(vehicleCols, a):
                        vehicles[key][col] = e

            responseDict = vehicles
            print(responseDict)
            status = 200
    
        elif '/etaRequest' in path:
            # can ask about eta based on vid and oid
            # cannot ask with no parameters
            statement = '''SELECT type, vid, custid, orderid,
                        start_lat, start_lon, end_lat, end_lon,
                        start_time, status
                        FROM dispatch WHERE '''
            if 'vid' in paramKeys:
                vid = paramDict['vid']
                statement += f'vid = {vid}'

            elif 'oid' in paramKeys:
                oid = paramDict['oid']
                statement += f'orderid = {oid}'

            cursor = sqlConnection.cursor()
            cursor.execute(statement)
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
        
            responseDict = {
                'ETA': eta
                }
            print(responseDict)
            status = 200
    
        elif '/getDispatch' in path:
            vid = paramDict['vid']
            statement = '''SELECT did, orderid, end_lat, end_lon,
                        status, start_time, type
                        FROM dispatch WHERE vid = %s'''
            cursor = sqlConnection.cursor()
            cursor.execute(statement, vid)
            dispatchTup = cursor.fetchall()
            cursor.close()
            renderCols = []
            for row in dispatchTup:
                lat = row[2]
                lon = row[3]
                # insert human readable here
                revGeo = None
                parsed = [row[0], row[1], revGeo, row[4], row[5], row[6]]
                renderCols.append(parsed)
        
            responseDict = renderCols
            print(responseDict)
            status = 200
    
        else:
            status = 404
    
        sqlConnection.close()
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
