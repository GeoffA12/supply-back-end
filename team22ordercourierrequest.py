import http.server
import json
from http.server import BaseHTTPRequestHandler

from copy import deepcopy
from dispatch import Dispatch

import utils.databaseutils as databaseutils
from utils.mappingutils import getETA, getRoute
from enums.vehiclestatus import VehicleStatus
from enums.dispatchstatus import DispatchStatus
from enums.servicetype import ServiceType


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ver = '0.1.0'

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

        # Pulling in our postbody data
        postBody = self.getPOSTBody()
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
            print(allPostions)
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
            etas = {vid: getETA(
                    startLat=lat,
                    startLon=lon,
                    endLat=dispatchDict['loc_f'][LAT_INDEX],
                    endLon=dispatchDict['loc_f'][LON_INDEX])
                for lat, lon, vid in allPostions}
            print(etas)
            fastestVID = sorted(etas.items(), key=lambda x: x[1])[0][0]
            # fastestVID, eta = sorted(etas.items(), key=lambda x: x[1])[0]
            print(fastestVID)

            if needsToBeQueued:
                dispatchDict['status'] = DispatchStatus.QUEUED

            # For now we are just picking the vehicle whose vid was just determined to have the fastest ETA to the
            # incoming orders destination
            vehicle = [vehicle for vehicle in vehicleEntries if vehicle[0] == fastestVID][0]
            print(vehicle)

            # Capture vehicle tuple into its separate variables
            vid, licensePlate, make, model, vLat, vLon = vehicle

            if not needsToBeQueued:
                # Now that a vehicle has been assigned their status will be updated, given that they weren't already
                # active
                databaseutils.updateVehicleStatus(vid)

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

        self.send_response(status)
        self.end_headers()
        res = json.dumps(responseBody)
        bytesStr = res.encode('utf-8')
        self.wfile.write(bytesStr)


def main():
    port = 4021
    # Create an http server using the class and port you defined
    httpServer = http.server.HTTPServer(('', port), SimpleHTTPRequestHandler)
    print("Running on port", port)
    # this next call is blocking! So consult with Devops Coordinator for
    # instructions on how to run without blocking other commands frombeing
    # executed in your terminal!
    httpServer.serve_forever()


if __name__ == '__main__':
    main()
