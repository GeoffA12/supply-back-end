import http.server
import json
import threading
import time
import urllib.parse as urlparser
from copy import deepcopy
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from dispatch import Dispatch
from enums.vehiclestatus import VehicleStatus
from enums.dispatchstatus import DispatchStatus
from enums.servicetype import ServiceType
from utils.serverutils import connectToSQLDB, notifications
from utils.vehicleutils import getEta


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.5.1'
    
    # How to convert the body from a string to a dictionary
    # use 'loads' to convert from byte/string to a dictionary!
    def getPOSTBody(self):
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        return json.loads(body)
    
    def do_POST(self):
        path = self.path
        print(path)
        status = 404

        # Pulling in our postbody data and opening up our SQL connection
        postBody = self.getPOSTBody()
        sqlConnection = connectToSQLDB()
        cursor = sqlConnection.cursor(buffered=True)
        responseBody = {}
        print(postBody)

        # Endpoint for when an order is submitted to dispatch a vehicle
        if '/vehicleRequest' in path:
            status = 200

            # First convert our string into the ServiceType enumerated type
            postBody['serviceType'] = ServiceType.translate(postBody['serviceType'])
            print(postBody['serviceType'])

            data = [VehicleStatus.INACTIVE.value, postBody['serviceType'].value, ]
            # print(data)
            # Query all vehicles whose status is INACTIVE and are a part of the fleet whose ServiceType is the
            # incoming order's service type
            # We need a switch here to know whether our dispatch should be inserted as QUEUED or RUNNING for the case
            # were there are no INACTIVE vehicles to pick up the order
            needsToBeQueued = False
            statement = '''SELECT vid, licenseplate,
                        make, model, current_lat, current_lon
                        FROM vehicles, fleets
                        WHERE vehicles.status = %s AND type = %s
                        AND vehicles.fleetid = fleets.fleetid'''
            cursor.execute(statement, tuple(data))
            vehicleEntries = cursor.fetchall()

            # In the case that we have no inactive vehicles, we then ask for the active vehicles and later on,
            # instead of a running dispatch, it will be queued.
            if not vehicleEntries:
                needsToBeQueued = True
                data[0] = VehicleStatus.ACTIVE.value
                cursor.execute(statement, tuple(data))
                vehicleEntries = cursor.fetchall()

            print(vehicleEntries)
            allPostions = [(x[4], x[5]) for x in vehicleEntries]

            # For now we are just picking the first vehicle of our vehicle list
            vehicle = vehicleEntries[0]

            # Capture vehicle tuple into its separate variables
            vid, licensePlate, make, model, vLat, vLon = vehicle

            if not needsToBeQueued:
                # Now that a vehicle has been assigned, their status will be updated, of course given that they
                # weren't already active
                print('updating vehicle status')
                statement = 'UPDATE vehicles SET status = 1'
                cursor.execute(statement)
                sqlConnection.commit()

            # Seeing if the unpacking worked d:
            print(vehicle)

            print(vid)
            print(licensePlate)
            print(make)
            print(model)
            print(vLon)
            print(vLat)

            # Need to convert to float as SQL's return type on floats are Decimal(...)
            vLat = float(vLat)
            vLon = float(vLon)

            # Getting our vehicle's eta!
            eta = getEta()[1]
            print(eta)

            # Organising our courier into a dictionary for our response body
            vehicleDict = {
                'vid': vid,
                'licensePlate': licensePlate,
                'make': make,
                'model': model,
                'curLocation': {
                    'lat': vLat,
                    'lon': vLon
                    },
                'ETA': eta
                }

            print(vehicleDict)

            # We are deepcopying so that we reuse and mutate components of our postBody, but also maintain the
            # postBody's immutability
            dispatchDict = deepcopy(postBody)
            dispatchDict['vid'] = vid

            # Turn the postBody's destination dictionary into a tupled pair
            destination = dispatchDict.pop('destination')
            dispatchDict['loc_f'] = (destination['lat'], destination['lon'])
            dispatchDict['loc_0'] = (vLat, vLon)
            if needsToBeQueued:
                dispatchDict['status'] = DispatchStatus.QUEUED

            print(dispatchDict)

            # Instantiating a dispatch instance
            dispatch = Dispatch(**dispatchDict)

            print(dispatch)

            LAT_INDEX = 0
            LON_INDEX = 1
            data = (
                dispatch.vid, dispatch.custid, dispatch.orderid,
                dispatch.loc_0[LAT_INDEX], dispatch.loc_0[LON_INDEX],
                dispatch.loc_f[LAT_INDEX], dispatch.loc_f[LON_INDEX],
                dispatch.timeCreated, dispatch.status.value, dispatch.serviceType.value,
                )
            # Now to add the new dispatch into the database
            statement = '''INSERT INTO dispatch
                        VALUES (Null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(statement, data)
            sqlConnection.commit()
            
            responseBody = vehicleDict
        
        elif '/addVehicle' in path:
            status = 200
            data = []
            # Because we are support the adding of multiple vehicles into our database in a single request,
            # and because of the formatting that SQL requires for an execution like this, we are going to iterate
            # through our postBody, put the values into a tuple, and then append that tuple into our data list. In
            # addition, we are going to set the 'default' status of the vehicle to INACTIVE
            for vehicleDict in postBody:
                # This is Steds btw d: ==> 30.2264, 97.7553,
                entry = (VehicleStatus.INACTIVE.value, vehicleDict['licensePlate'], vehicleDict['fleetid'],
                         vehicleDict['make'], vehicleDict['model'],
                         30.2264, 97.7553, None, vehicleDict['dateAdded'].replace('T', ' ').replace('Z', ' '))
                data.append(entry)
            print(data)
            statement = '''INSERT INTO vehicles
                        VALUES (Null, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.executemany(statement, data)
            sqlConnection.commit()

        elif '/removeVehicle' in path:
            status = 200
            data = [(vid,) for viddict in postBody for vid in viddict.values()]

            print(data)
            statement = 'DELETE FROM vehicles WHERE vid = %s'
            cursor.executemany(statement, data)
            sqlConnection.commit()

        elif '/updateVehicle' in path:
            allowableUpdates = {'status', 'licenseplate', 'fleetid', 'current_lat', 'current_lon', 'last_heartbeat'}
            status = 401
    
            vidless = deepcopy(postBody)
            vid = vidless.pop('vid')
            if 'vid' in postBody and vidless and set(vidless.keys()).issubset(allowableUpdates):
                statement = 'SELECT * FROM vehicles WHERE vid = %s'
                cursor.execute(statement, (vid,))
                entry = cursor.fetchone()[0]
                if entry:
                    status = 200
                    statement = 'UPDATE vehicles SET'
                    data = []
                    for key, value in postBody.items():
                        if key is 'status':
                            value = VehicleStatus.translate(value).value
                        statement += f' {key} = %s,'
                        data.append(value)

                    statement = statement[:-1]
                    statement += ' WHERE vid = %s'
                    data.append(vid)

                    print(statement)
                    print(data)

                    cursor.execute(statement, tuple(data))
                    sqlConnection.commit()

        elif '/addFleet' in path:
            status = 200

            emailOrUser = postBody['username']
            region = postBody['region']
            serviceType = postBody['serviceType']

            # Because fleets utilise a fleet manager id and not their email or username, we'll need to retrieve that
            # first using the incoming username/email. We will support both
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
        cursor = sqlConnection.cursor(buffered=True)
        responseBody = {}
        '''
        The addition of parameters will apply a filtering process
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
                if 'fmid' in paramsDict:
                    users = paramsDict['fmid']
        
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
            # print(responseBody)
            status = 200
            for vehicle in responseBody:
                for k, v in vehicle.items():
                    print(k, v)

        elif '/fleets' in path:
            statement = 'SELECT * FROM fleets'
            cursor.execute(statement)
            rows = cursor.fetchall()
            fleets = [list(x) for x in rows]
    
            if hasParams:
                if 'fmid' in paramsDict:
                    fmids = set(paramsDict['fmid'])
                    fleets = [fm for fmid in fmids for fm in rows if int(fmid) == fm[3]]
    
            fleetColNames = ['fleetid', 'region', 'serviceType', 'fmid']
    
            fleetDictList = []
            for fleet in fleets:
                fleetDict = {}
                for colName, colVal, in zip(fleetColNames, fleet):
                    fleetDict[colName] = colVal
                fleetDictList.append(fleetDict)
    
            responseBody = fleetDictList
            # print(responseBody)
            status = 200
            for fleet in responseBody:
                for k, v in fleet.items():
                    print(k, v)

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
                print('tup:', dispatchTup)
                if dispatchTup is not None:
                    temp = [list(x) for x in dispatchTup]
                    dispatches.extend(temp)

            print(dispatches)
            dispatchesCopy = deepcopy(dispatches)

            dispatches = []
            for dispatch in dispatchesCopy:
                print('dispatch', dispatch)
                startLat, startLon = dispatch.pop(4), dispatch.pop(4)
                startHuman = 'St. Edward\'s University'
                startDict = {
                    'humanReadable': startHuman,
                    'lat': float(startLat),
                    'lon': float(startLon)
                    }

                endLat, endLon = dispatch.pop(4), dispatch.pop(4)
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


def healthChecker():
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor()
    statement = 'SELECT fleetid, fmid FROM fleets;'
    cursor.execute(statement)
    rows = cursor.fetchall()
    cursor.close()
    sqlConnection.close()
    print(rows)
    for fleetData in rows:
        thread = threading.Thread(target=heartbeatListener, args=fleetData)
        thread.start()


def heartbeatListener(fleetid, fmid):
    print(f'Listener for Fleet {fleetid} has started')
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = "SELECT email FROM fleetmanagers WHERE fmid = %s"
    cursor.execute(statement, (fmid,))
    email = cursor.fetchone()[0]
    cursor.close()
    sqlConnection.close()
    CHECKER_INTERVAL = 45
    missedHeartbeats = {}
    try:
        while True:
            time.sleep(CHECKER_INTERVAL)
            sqlConnection = connectToSQLDB()
            cursor = sqlConnection.cursor(buffered=True)

            statement = "SELECT vid, last_heartbeat FROM vehicles WHERE fleetid = %s AND status <> 3"
            cursor.execute(statement, (fleetid,))
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            sqlConnection.close()

            d = {k: v for (k, v) in rows}
            for vid, lasthb in d.items():
                if lasthb is not None:
                    now = datetime.now()
                    difference = now - lasthb
                    minutes = difference.seconds / 60
                    print(f'Difference in minutes: {round(minutes, 4)}')
                    if difference > timedelta(minutes=5):
                        print(f'Vehicle ID: {vid} hasn\'t reported in for at least 5 minutes!')

                        subject = f'Vehicle ID: {vid} hasn\'t reported in for {round(minutes, 2)}'
                        body = f'Vehicle ID: {vid} hasn\'t reported in for {round(minutes, 2)}'
                        notifications(recipients=email,
                                      subject=subject,
                                      body=body)
                else:
                    print('vehicle just added and hasn\'t spun up a heartbeat')
                    # notifications(recipients=email, subject='hi', body='hi')

    except KeyboardInterrupt:
        raise
    finally:
        print(f'Listener for Fleet {fleetid} is ending')


def main():
    port = 4022
    # Create an http server using the class and port you defined
    httpServer = http.server.HTTPServer(('', port), SimpleHTTPRequestHandler)
    print("Running on port", port)
    # this next call is blocking! So consult with Devops Coordinator for
    # instructions on how to run without blocking other commands frombeing
    # executed in your terminal!
    print('I got here')
    healthChecker()
    print('healthChecker initialised')
    httpServer.serve_forever()


if __name__ == '__main__':
    main()
    # print('I got here')
    # healthChecker()
    # print('healthChecker initialised')
