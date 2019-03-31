from uszipcode import SearchEngine

#declare a basic global search variable
search = SearchEngine(simple_zipcode=True)

def zip_to_coords(zipInput):

    zipcode = search.by_zipcode(zipInput)
    zip_dict = zipcode.to_dict()
    #print("dict: ", zip_dict)

    latitude = zip_dict["lat"]
    longitude = zip_dict["lng"]
    #print(latitude, " ", longitude)
    return latitude, longitude

def zip_to_city_state(zipcode):
    city_state = search.by_zipcode(zipcode).to_dict()
    #print("dict: ", city_state)

    city = city_state["major_city"]
    state = city_state["state"]
    #print("city: ", city, " state: ", state)

    return city, state

def city_to_city_state(city):
    city_state = (search.by_city(city)[0]).to_dict()

    city = city_state["major_city"]
    state = city_state["state"]

    return city, state

def main(city, state):
    print("City: ", city, " State: ", state)
    zipcode = search.by_city_and_state(city, state)[0]
    #print("zip: ", zipcode)

    return zip_to_coords(zipcode)
