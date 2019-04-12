from uszipcode import SearchEngine
search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database


def main(userlocation):
    """Takes a string containing a ZIP code, 'City, State', or 'City' and returns the latitude and longitude"""

    # Determine if the location string provided by the user is a ZIP code or city. If int, assume ZIP, else assume city.
    if userlocation.isdigit():
        locationlookup = search.by_zipcode(userlocation)

    # If the input is not an integer, we will assume it is a "city, state" or just "city".  There are two methods to
    # search for 'city, state', and so we will try the faster method first, which is where the function expects there to
    # be in the format "city, state."  If the user only enters a city name, we will use the slowest and last method.
    elif ',' in userlocation:
        # Let's split the string and grab the city and state
        citystate = [x.strip() for x in userlocation.split(',')]
        city = citystate[0]
        state = citystate[1]

        locationlookup = search.by_city_and_state(city, state)

        # When passing in a city name, if it is not found, an empty list is returned, so check that the list isn't empty


        # For some reason, the uszipcode module handles city input differently, and returns a list. Let's strip that off
        locationlookup = locationlookup[0]

    # If the user supplies only a city name, do the slow search
    else:
        locationlookup = search.by_city(userlocation)
        # When passing in a city name, if it is not found, an empty list is returned, so check that the list isn't empty
        if not locationlookup:
            return None, None, 'Unrecognized location'

        # For some reason, the uszipcode module handles city input differently, and returns a list. Let's strip that off
        locationlookup = locationlookup[0]

    # The uszipcode module returns a big list of values that we don't need.  We only want latitude and longitude.
    location_dict = locationlookup.to_dict()

    latitude = location_dict["lat"]
    longitude = location_dict["lng"]
    # If a state is not provided, this will let the user know what city their query returned
    cityfound = location_dict["post_office_city"]

    # An invalid ZIP code will result in a list of 'None' values, so that is how we will check if the ZIP is valid.
    if latitude is None:
        return None, None, 'Unrecognized location'

    else:
        return latitude, longitude, cityfound
