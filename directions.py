import openrouteservice

coords = ((8.34234,48.23424),(8.34423,48.26424))

client = openrouteservice.Client(key='5b3ce3597851110001cf62483b4bbad3ed8247c3b973b8a1471cac8e') # Specify your personal API key
routes = client.directions(coords)

print(routes)
