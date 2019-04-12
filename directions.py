import openrouteservice
import zip_converter
from api_keys import route_key, geo_key

def locate(destination):    

    #find user's current location
    startingGeocoder = geocoder.ip('me')
    startingLatitude = startingGeocoder.lat
    startingLongitude = startingGeocoder.lng
    startingPosition = (startingLatitude, startingLongitude)

    #find the coordinates of the desired location
    endingGeocoder = geocoder.mapquest(destination, key=geo_key)
    endingLatitude = endingGeocoder[0].lat
    endingLongitude = endingGeocoder[0].lng
    endPosition = (endingLongitude, endingLatitude)

    coordinates = (startingPosition, endPosition)
    print(coordinates)

    client = openrouteservice.Client(route_key)
    routes = client.directions(coordinates, units="mi", profile="driving-car")

    #format direction output
    output = ""
    for route in routes["routes"][0]["segments"][0]["steps"]:
        output += "In " + str(route["distance"]) + " miles, " + route["instruction"] + ".\n"

    return output

#print(locate("Memorial Union University of Rhode Island"))
