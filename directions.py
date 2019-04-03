import geocoder

def locate(destination):
    import openrouteservice
    geo_key = "2kqkK0njHHY1OZIQyqGpb3JAB83migj6"

    #find user's current location
    sg = geocoder.ip('me')
    s_lat = sg.lat
    s_lng = sg.lng
    start_pos = (s_lng, s_lat)

    #find the coordinates of the desired location
    eg = geocoder.mapquest(destination, key=geo_key)
    e_lat = eg[0].lat
    e_lng = eg[0].lng
    end_pos = (e_lng, e_lat)

    coords = (start_pos, end_pos)
    print(coords)

    route_key = '5b3ce3597851110001cf62483b4bbad3ed8247c3b973b8a1471cac8e'
    client = openrouteservice.Client(route_key)
    routes = client.directions(coords, units="mi")

    #format direction output
    output = ""
    for route in routes["routes"][0]["segments"][0]["steps"]:
        output += "In " + str(route["distance"]) + " miles, " + route["instruction"] + ".\n"

    return output

print(locate("Narragansett Beach"))

