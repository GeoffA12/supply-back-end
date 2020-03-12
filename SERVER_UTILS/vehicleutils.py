import requests
import json


# route request API
def getRoute():
    # Make request for mapbox driving data given two coordinates
    mapbox_driving_req = requests.get(
        'https://api.mapbox.com/directions/v5/mapbox/driving/-97.724208,30.306963;-97.760131,'
        '30.328231?geometries=geojson&access_token=pk.eyJ1IjoiY3N5Y2hldiIsImEiOiJjazZsbmg4c2gwYXU3M21zOG55aTljcTBuIn0'
        '.G5UXjF-3_0mXKo6huFgLwg')
    # encode data
    data = mapbox_driving_req.json()
    # json dump coordinates data
    coords = json.dumps(data.get("routes")[0].get("geometry").get("coordinates"))
    return coords


# eta request API
def getEta():
    # Make request for mapbox driving data given two coordinates
    mapbox_driving_req = requests.get(
        'https://api.mapbox.com/directions/v5/mapbox/driving/-97.724208,30.306963;-97.760131,'
        '30.328231?geometries=geojson&access_token=pk.eyJ1IjoiY3N5Y2hldiIsImEiOiJjazZsbmg4c2gwYXU3M21zOG55aTljcTBuIn0'
        '.G5UXjF-3_0mXKo6huFgLwg')
    # encode data
    data = mapbox_driving_req.json()
    # json dump distance traveled along route data and cast it as a float
    # distance is given in meters
    distance = float(json.dumps(data.get("routes")[0].get("distance")))
    # calculate mock eta from distance data with mock mph
    eta = ((distance / 1609.34) / 30) * 60
    # print("ETA IS:", "%.2f" % eta, "MINUTES")
    return "ETA IS:", "%.2f" % eta, "MINUTES"


# heartbeat not implemented in this utils yet
def heartbeat():
    return "healthcheck data"
