from uszipcode import SearchEngine

def main(city, state):
    search = SearchEngine(simple_zipcode=True)

    #print(city, " ", state)
    zipcode = search.by_city_and_state(city, state)[0]
    #print("city: ", zipcode)

    zip_dict = zipcode.to_dict()
    #print("dict: ", zip_dict)

    latitude = zip_dict["lat"]
    longitude = zip_dict["lng"]
    #print(latitude, " ", longitude)
    return latitude, longitude