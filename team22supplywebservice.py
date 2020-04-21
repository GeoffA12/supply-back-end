import http.server
import json
import urllib.parse as urlparser
from copy import deepcopy
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import utils.databaseutils as databaseutils

from utils.serverutils import notifications, healthChecker
from enums.vehiclestatus import VehicleStatus
from dispatch import Dispatch


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.5.4'

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
        responseBody = {}
        print(postBody)

        if '/supply/vehicles/add' in path:
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

        elif '/supply/vehicles/rem' in path:
            status = 200
            # Extract the vids from the postBody and store it into a list.
            vehicleData = [(vid,) for viddict in postBody for vid in viddict.values()]

            # print(vehicleData)
            databaseutils.delVehicle(vehicleData)

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

                    if 'last_heartbeat' in postBody.keys():
                        dispatchTup = databaseutils.getRunningDispatchByVID(vid)
                        dispatchDict = {
                            'serviceType': dispatchTup[10],
                            'vid': dispatchTup[1],
                            'custid': dispatchTup[2],
                            'orderid': dispatchTup[3],
                            'loc_0': (float(dispatchTup[4]), float(dispatchTup[5]),),
                            'loc_f': (float(dispatchTup[6]), float(dispatchTup[7])),
                            'timeCreate': dispatchTup[8],
                        }
                        dispatch = Dispatch(**dispatchDict)
                        responseBody = [dispatchTup[0], dispatch.route]

        elif '/supply/fleets/add' in path:
            status = 200

            emailOrUser = postBody['username']
            region = postBody['region']
            serviceType = postBody['serviceType']

            # Because fleets utilise a fleet manager id and not their email or username, we'll need to retrieve that
            # first using the incoming username/email. We will support both
            fmid = databaseutils.getFMID(emailOrUser)
            fleetData = (region, serviceType, fmid,)
            print(fleetData)
            databaseutils.addFleet(fleetData)

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

        responseBody = {}
        '''
        The addition of parameters will apply a filtering process
        '''

        if '/supply/vehicles' in path:
            rows = databaseutils.getAllVehicles()
            vehicles = [list(x) for x in rows]

            # print(vehicles)
            if hasParams:
                # Parameter for fleet master
                if 'user' in paramsDict:
                    users = paramsDict['user']

                    usersCopy = deepcopy(users)
                    users = [(x, x) for x in usersCopy]
                    print(users)
                    fleetIDs = databaseutils.getFleetIDByFMCredentials(users)
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

            print(vehicles)

            vehicleColsNames = ['vehicleid', 'status', 'licenseplate', 'fleetid', 'make', 'model',
                                'current_lat', 'current_lon', 'last_heartbeat', 'date_added']

            vehiclesDictList = []
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
            # for vehicle in responseBody:
            #     for k, v in vehicle.items():
            #         print(k, v)

        elif '/supply/fleets' in path:
            rows = databaseutils.getAllFleets()
            fleets = [list(x) for x in rows]

            if hasParams:
                if 'user' in paramsDict:
                    users = paramsDict['user']
                    `
                    fleetIDs = databaseutils.getFleetIDByFMCredentials(users)
                    fleets = [fleet for fleetID in set(fleetIDs) for fleet in rows if int(fleetID) == fleet[0]]

                elif 'fmid' in paramsDict:
                    fmids = set(paramsDict['fmid'])
                    fleets = [fleet for fmid in fmids for fleet in rows if int(fmid) == fleet[3]]

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
            # for fleet in responseBody:
            #     for k, v in fleet.items():
            #         print(k, v)

        elif '/supply/dispatch' in path:
            vids = paramsDict['vid']
            print(vids)

            vidsCopy = deepcopy(vids)
            vids = [(x,) for x in vidsCopy]
            print(vids)
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
            # for dispatch in responseBody:
            #     for k, v in dispatch.items():
            #         print(k, v)

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
