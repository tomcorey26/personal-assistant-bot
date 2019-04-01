from darksky import forecast
import zip_converter
from api_keys import *


class forcasts:

    # class constructor to get values
    def __init__(self, lat, lng, date, timedelta):
        self.LOCATION = lat, lng
        self.date = date
        self.timedelta = timedelta

    # method to take in the location, date, and timedelta and will put back the weekly forcast, aka 7 day forcast
    def weeklyForcast(self):
        # calls the darksky api giving it the location(latitude and longitude) and the api key
        with forecast(DARK_SKY_KEY, *self.LOCATION) as location:
            # formats the weeks data into a dictionary for easy information access
            # day becomes the dictionary of the current date, the summary of the day
            # the min temp of the day and the max temp of the day
            hour = dict(hour=self.date.strftime(str(self.date)),
                        sum=location.summary,
                        temp=location.temperature
                        )
            # the dictionaries information is formatted and printed out to the user
            curr_temp = '{temp}'.format(**hour).lower()
            curr_sum = '{sum}'.format(**hour).lower()
            # increments the date by the timedelta
        return curr_temp, curr_sum


    # returns the location we are currently concerned with
    def getLocation(self):
        return self.LOCATION

    # returns the date we are currently concerned with
    def getDate(self):
        return self.date

    # returns the timedelta we are currently concerned with
    def getTimeDelta(self):
        return self.timedelta

def getCurrentWeather(lat, lon):
    currentForecast = forecast(DARK_SKY_KEY, lat, lon)

    temp = currentForecast.temperature
    summ = currentForecast.summary
    icon = currentForecast.icon
    humidity = currentForecast.humidity

    return temp, summ, icon, humidity

def main(lat, lng):
    # imports the datetime library with the fields date and timedelta
    from datetime import date, timedelta

    # sets the date to today's date
    date = date.today()

    # creates a forcasts object from the forcasts class
    forcast = forcasts(lat, lng, date, timedelta)

    temperature, summary = forcast.weeklyForcast()

    return temperature, summary

print(main(41.4476, -71.5247))