import geocoder
from api_keys import geo_key, route_key

def locate(destination):
    import openrouteservice
    

    #find user's current location
    startGeocoder = geocoder.ip('me')
    s_lat = startGeocoder.lat
    s_lng = startGeocoder.lng
    start_pos = (s_lng, s_lat)

    #find the coordinates of the desired location
    eg = geocoder.mapquest(destination, key=geo_key)
    e_lat = eg[0].lat
    e_lng = eg[0].lng
    end_pos = (e_lng, e_lat)

    coords = (start_pos, end_pos)
    print(coords)

    client = openrouteservice.Client(route_key)
    routes = client.directions(coords, units="mi", profile="driving-car")

    #format direction output
    output = ""
    for route in routes["routes"][0]["segments"][0]["steps"]:
        output += "In " + str(route["distance"]) + " miles, " + route["instruction"] + ".\n"

    return output

#print(locate("Memorial Union University of Rhode Island"))
