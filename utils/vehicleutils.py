import requests
import json


def getDriverJSON(startLat=None, startLon=None, endLat=None, endLon=None):
    token = 'pk.eyJ1IjoiY3N5Y2hldiIsImEiOiJjazZsbmg4c2gwYXU3M21zOG55aTljcTBuIn0.G5UXjF-3_0mXKo6huFgLwg'
    urlHead = 'https://api.mapbox.com/directions/v5/mapbox/driving/'
    urlTail = '?geometries=geojson&access_token='
    url = f'{urlHead}{startLon},{startLat};{endLon},{endLat}{urlTail}{token}'
    mapbox_driving_req = requests.get(url)
    return mapbox_driving_req.json()


# route request API
def getRoute(startLat=None, startLon=None, endLat=None, endLon=None):
    # Make request for mapbox driving data given two coordinates
    # encode data
    # print(data)
    data = getDriverJSON(startLat=startLat,
                         startLon=startLon,
                         endLat=endLat,
                         endLon=endLon)
    # json dump coordinates data
    coords = json.dumps(data.get("routes")[0].get("geometry").get("coordinates"))
    return coords


# eta request API
def getETA(startLat=None, startLon=None, endLat=None, endLon=None):
    # Make request for mapbox driving data given two coordinates
    # encode data
    data = getDriverJSON(startLat=startLat,
                         startLon=startLon,
                         endLat=endLat,
                         endLon=endLon)
    # json dump distance traveled along route data and cast it as a float
    # distance is given in meters
    print(data)
    distance = float(json.dumps(data.get("routes")[0].get("distance")))
    # calculate mock eta from distance data with mock mph
    eta = ((distance / 1609.34) / 30) * 60
    print("ETA IS:", "%.2f" % eta, "MINUTES")
    return round(eta, 2)


# heartbeat not implemented in this utils yet
def heartbeat():
    return "healthcheck data"


#if __name__ == '__main__':
    #startCoor = (30.306963, -97.724208)
    #endCoor = (30.328231, -97.760131)
    #route = getRoute(startLat=startCoor[0],
    #                 startLon=startCoor[1],
    #                 endLat=endCoor[0],
    #                 endLon=endCoor[1])
    #print(route)
    
    #eta = getETA(startLat=startCoor[0],
    #             startLon=startCoor[1],
    #             endLat=endCoor[0],
    #             endLon=endCoor[1])
    #print(eta)
