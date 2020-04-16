import http.server
import json
import urllib.parse as urlparser
from copy import deepcopy
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from dispatch import Dispatch
from enums.vehiclestatus import VehicleStatus
from enums.dispatchstatus import DispatchStatus
from enums.servicetype import ServiceType
from utils.serverutils import notifications, healthChecker
from utils.mappingutils import getETA, getRoute
import utils.databaseutils as databaseutils


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.5.3'

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
        # sqlConnection = databaseutils.connectToSQLDB()
        # cursor = sqlConnection.cursor(buffered=True)
        responseBody = {}
        print(postBody)

        # Endpoint for when an order is submitted to dispatch a vehicle
        if '/supply/vehicles/req' in path:
            status = 200

            # First convert our string into the ServiceType enumerated type
            postBody['serviceType'] = ServiceType.translate(postBody['serviceType'])
            print(postBody['serviceType'])

            desiredVehicleAttributes = [VehicleStatus.INACTIVE.value, postBody['serviceType'].value, ]
            # print(desiredVehicleAttributes)
            # Query all vehicles whose status is INACTIVE and are a part of the fleet whose ServiceType is the
            # incoming order's service type
            # We need a switch here to know whether our dispatch should be inserted as QUEUED or RUNNING for the case
            # were there are no INACTIVE vehicles to pick up the order
            vehicleEntries = databaseutils.getCourierCandidates(desiredVehicleAttributes)

            needsToBeQueued = False
            # In the case that we have no inactive vehicles, we then ask for the active vehicles and later on,
            # instead of a running dispatch, it will be queued.
            if not vehicleEntries:
                needsToBeQueued = True
                desiredVehicleAttributes[0] = VehicleStatus.ACTIVE.value
                vehicleEntries = databaseutils.getCourierCandidates(desiredVehicleAttributes)

            print(vehicleEntries)
            # Make a tuple containing all the returned vehicles' current lat, lon and vid
            allPostions = [(float(x[4]), float(x[5]), x[0]) for x in vehicleEntries]

            # We are deepcopying so that we reuse and mutate components of our postBody, but also maintain the
            # postBody's immutability
            dispatchDict = deepcopy(postBody)

            # Turn the postBody's destination dictionary into a tupled pair
            destination = dispatchDict.pop('destination')
            dispatchDict['loc_f'] = (destination['lat'], destination['lon'])

            LAT_INDEX = 0
            LON_INDEX = 1
            # Create a dictionary where the keys are vids and the values are the derived ETAs based on the returned
            # cars' current position to the order's destination
            etas = {vid: getETA(startLat=lat,
                    startLon=lon,
                    endLat=dispatchDict['loc_f'][LAT_INDEX],
                    endLon=dispatchDict['loc_f'][LON_INDEX])
                    for lat, lon, vid in allPostions}
            print(etas)
            fastestVID = sorted(etas.items(), key=lambda x: x[1])[0][0]
            print(fastestVID)

            if needsToBeQueued:
                dispatchDict['status'] = DispatchStatus.QUEUED

            # For now we are just picking the first vehicle of our vehicle list
            vehicle = [vehicle for vehicle in vehicleEntries if vehicle[0] == fastestVID][0]
            print(vehicle)

            # Capture vehicle tuple into its separate variables
            vid, licensePlate, make, model, vLat, vLon = vehicle

            if not needsToBeQueued:
                # Now that a vehicle has been assigned their status will be updated, given that they weren't already
                # active
                databaseutils.updateVehicleStatus(vid)
                # statement = 'UPDATE vehicles SET status = 1 where vid = %s'
                # cursor.execute(statement, (vid,))
                # sqlConnection.commit()

            # Seeing if the unpacking worked d:
            print(vehicle)

            print(vid)
            print(licensePlate)
            print(make)
            print(model)
            print(vLon)
            print(vLat)

            # Need to convert to float as SQL's return type on floats are Decimal(...)
            # vLat = float(vLat)
            # vLon = float(vLon)

            # These are added here because until this point we have no idea which vehicle would carry out the order
            # Everything else in the post body was already almost already how it needed to be to translate directly to
            # a dispatch dictionary
            dispatchDict['loc_0'] = (vLat, vLon)
            dispatchDict['vid'] = vid

            print(dispatchDict)

            # Instantiating a dispatch instance
            dispatch = Dispatch(**dispatchDict)

            print(dispatch)

            dispatchData = (
                dispatch.vid, dispatch.custid, dispatch.orderid,
                dispatch.loc_0[LAT_INDEX], dispatch.loc_0[LON_INDEX],
                dispatch.loc_f[LAT_INDEX], dispatch.loc_f[LON_INDEX],
                dispatch.timeCreated, dispatch.status.value, dispatch.serviceType.value,
            )
            # Now to add the new dispatch into the database
            databaseutils.storeDispatch(dispatchData)
            # statement = 'INSERT INTO dispatch VALUES (Null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            # cursor.execute(statement, dispatchData)
            # sqlConnection.commit()

            # Getting our vehicle's eta!
            eta = dispatch.getETA(dispatch.loc_0)
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

            responseBody = vehicleDict

        elif '/supply/vehicles/add' in path:
            status = 200
            vehicleData = []
            # Because we are support the adding of multiple vehicles into our database in a single request,
            # and because of the formatting that SQL requires for an execution like this, we are going to iterate
            # through our postBody, put the values into a tuple, and then append that tuple into our vehicleData list. In
            # addition, we are going to set the 'default' status of the vehicle to INACTIVE
            for vehicleDict in postBody:
                # This is Steds btw d: ==> 30.2264, -97.7553,
                entry = (VehicleStatus.INACTIVE.value, vehicleDict['licensePlate'], vehicleDict['fleetid'],
                         vehicleDict['make'], vehicleDict['model'],
                         30.2264, -97.7553, None, vehicleDict['dateAdded'].replace('T', ' ').replace('Z', ' '))
                vehicleData.append(entry)
            # print(vehicleData)
            databaseutils.addVehicle(vehicleData)
            # statement = 'INSERT INTO vehicles VALUES (Null, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            # cursor.executemany(statement, vehicleData)
            # sqlConnection.commit()

        elif '/supply/vehicles/rem' in path:
            status = 200
            # Extract the vids from the postBody and store it into a list.
            vehicleData = [(vid,) for viddict in postBody for vid in viddict.values()]

            # print(vehicleData)
            databaseutils.delVehicle(vehicleData)
            # statement = 'DELETE FROM vehicles WHERE vid = %s'
            # cursor.executemany(statement, vehicleData)
            # sqlConnection.commit()

        elif '/supply/vehicles/upd' in path:
            allowableUpdates = {'status', 'licenseplate', 'fleetid', 'current_lat', 'current_lon', 'last_heartbeat'}
            status = 401

            vidless = deepcopy(postBody)
            vid = vidless.pop('vid')

            # Need to check if the vid is in the postBody bc we won't know what vehicle to update without it
            # Need to make sure that there are attributes that want to be updated
            # The desired attributes to be updated must be a part of the set of
            # attributes that are allowed to be updated
            if 'vid' in postBody and vidless and set(vidless.keys()).issubset(allowableUpdates):
                entry = databaseutils.getVehicleByVID(vid)
                # statement = 'SELECT * FROM vehicles WHERE vid = %s'
                # cursor.execute(statement, (vid,))
                # entry = cursor.fetchone()[0]
                if entry:
                    status = 200
                    statement = 'UPDATE vehicles SET'
                    vehicleData = []

                    # Building an SQL UPDATE ... SET statement with the desired attributes and their values
                    for col, colVal in postBody.items():
                        if col is 'status':
                            colVal = VehicleStatus.translate(colVal).value
                        statement += f' {col} = %s,'
                        vehicleData.append(colVal)

                    # Pruning the statement for SQL formatting
                    statement = statement[:-1]
                    statement += ' WHERE vid = %s'
                    # Append vid at the end bc the where clause always goes at the end
                    vehicleData.append(vid)

                    print(statement)
                    print(vehicleData)

                    databaseutils.updVehicle(statement, vehicleData)

        elif '/supply/fleets/add' in path:
            status = 200

            emailOrUser = postBody['username']
            region = postBody['region']
            serviceType = postBody['serviceType']

            # Because fleets utilise a fleet manager id and not their email or username, we'll need to retrieve that
            # first using the incoming username/email. We will support both
            fmid = databaseutils.getFMID(emailOrUser)
            # statement = 'SELECT fmid FROM fleetmanagers WHERE email = %s OR username = %s'
            # data = (emailOrUser, emailOrUser,)
            # cursor.execute(statement, data)
            # fmid = cursor.fetchone()[0]
            fleetData = (region, serviceType, fmid,)
            print(fleetData)
            databaseutils.addFleet(fleetData)
            # statement = 'INSERT INTO fleets VALUES (Null, %s, %s, %s)'
            # cursor.execute(statement, fleetData)
            # sqlConnection.commit()

        # cursor.close()
        # sqlConnection.close()
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

        # sqlConnection = databaseutils.connectToSQLDB()
        # cursor = sqlConnection.cursor(buffered=True)
        responseBody = {}
        '''
        The addition of parameters will apply a filtering process
        '''

        if '/supply/vehicles' in path:
            # statement = 'SELECT * FROM vehicles'
            # cursor.execute(statement)
            # rows = cursor.fetchall()
            rows = databaseutils.getAllVehicles()
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
                    # statement = '''SELECT fleets.fleetid
                    #             FROM fleets, fleetmanagers
                    #             WHERE fleets.fmid = fleetmanagers.fmid
                    #             AND (fleetmanagers.username = %s
                    #             OR fleetmanagers.email = %s)'''
                    # fleetIDs = []
                    # for user in users:
                    #     cursor.execute(statement, user)
                    #     temp = cursor.fetchall()
                    #     flatten = [item for sublist in temp for item in sublist]
                    #     print(flatten)
                    #     fleetIDs.extend(flatten)d
                    #     print(fleetIDs)
                    # print(fleetIDs)
                    fleetIDs = (databaseutils.getFleetIDByFMCredentials(users))
                    vehicles = [vehicle for fleetID in set(fleetIDs) for vehicle in rows if fleetID == vehicle[3]]

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
                    # Filter all vehicles until you find the
                    vehicles = [vehicle for vehicleID in vids for vehicle in rows if int(vehicleID) == vehicle[0]]

                elif 'fid' in paramsDict:
                    fleetIDs = set(paramsDict['fid'])
                    print(fleetIDs)
                    print(rows)
                    vehicles = [vehicle for fleetID in fleetIDs for vehicle in rows if int(fleetID) == vehicle[3]]
                    fleetIDs = list(fleetIDs)

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
                    elif colName == 'last_heartbeat' and colName is not None:
                        colVal = str(colVal)
                    vehicleDict[colName] = colVal
                vehiclesDictList.append(vehicleDict)

            responseBody = vehiclesDictList
            # print(responseBody)
            status = 200
            for vehicle in responseBody:
                for k, v in vehicle.items():
                    print(k, v)

        elif '/fleets' in path:
            # statement = 'SELECT * FROM fleets'
            # cursor.execute(statement)
            # rows = cursor.fetchall()
            rows = databaseutils.getAllFleets()
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

        elif '/supply/dispatch' in path:
            vids = paramsDict['vid']
            print(vids)

            vidsCopy = deepcopy(vids)
            vids = [(x,) for x in vidsCopy]
            print(vids)
            # statement = '''SELECT * FROM dispatch WHERE vid = %s'''
            # print(statement)
            # dispatches = []
            # for vid in vids:
            #     cursor = sqlConnection.cursor()
            #     cursor.execute(statement, vid)
            #     dispatchTup = cursor.fetchall()
            #     print('tup:', dispatchTup)
            #     if dispatchTup is not None:
            #         temp = [list(x) for x in dispatchTup]
            #         dispatches.extend(temp)
            dispatches = databaseutils.getDispatchByVID(vids)
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

        # cursor.close()
        # sqlConnection.close()
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
    healthChecker()
    print('healthChecker initialised')
    httpServer.serve_forever()


if __name__ == '__main__':
    main()
