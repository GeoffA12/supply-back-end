import requests
import json

ver = '0.1.0'


def getDriverJSON(startLat=None, startLon=None, endLat=None, endLon=None):
    token = 'pk.eyJ1IjoiY3N5Y2hldiIsImEiOiJjazZsbmg4c2gwYXU3M21zOG55aTljcTBuIn0.G5UXjF-3_0mXKo6huFgLwg'
    urlHead = 'https://api.mapbox.com/directions/v5/mapbox/driving/'
    urlTail = '?geometries=geojson&access_token='
    url = f'{urlHead}{startLon},{startLat};{endLon},{endLat}{urlTail}{token}'
    mapbox_driving_req = requests.get(url)
    return mapbox_driving_req.json()


# route request API
def getRoute(startLat=None, startLon=None, endLat=None, endLon=None):
    import ast
    # Make request for mapbox driving data given two coordinates
    # encode data
    # print(data)
    data = getDriverJSON(startLat=startLat,
            startLon=startLon,
            endLat=endLat,
            endLon=endLon)
    # json dump coordinates data
    coords = json.dumps(data.get("routes")[0].get("geometry").get("coordinates"))
    return ast.literal_eval(coords)


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
    # print(data)
    try:
        distance = float(json.dumps(data.get("routes")[0].get("distance")))
    except:
        distance = 1_000_000_000
    # calculate mock eta from distance data with mock mph
    eta = ((distance / 1609.34) / 30) * 60
    print("ETA IS:", "%.2f" % eta, "MINUTES")
    return round(eta, 2)


def getHumanReadable(begin_long, begin_lat):
    # Make request for mapbox driving data given a set of coordinates
    mapbox_driving_req = requests.get(
            'https://api.mapbox.com/geocoding/v5/mapbox.places/' + str(begin_long) + ',' + str(
                    begin_lat) + '.json?access_token=pk.eyJ1IjoiY3N5Y2hldiIsImEiOiJjazZsbmg4c2gwYXU3M21zOG55aTljcTBuIn0.G5UXjF-3_0mXKo6huFgLwg&place_name')
    # encode data
    data = mapbox_driving_req.json()
    # json dump place name data
    address = json.dumps(data.get("features")[0].get('place_name'))
    return address
