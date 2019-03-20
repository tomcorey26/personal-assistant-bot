from darksky import forecast
import zip_converter
from api_keys import *


class forcasts:

    # class constructor to get values
    def __init__(self, LOCATION, date, timedelta):
        self.LOCATION = LOCATION
        self.date = date
        self.timedelta = timedelta

    # method to take in the location, date, and timedelta and will put back the weekly forcast, aka 7 day forcast
    def weeklyForcast(self):
        # calls the darksky api giving it the location(latitude and longitude) and the api key
        with forecast(DARK_SKY_KEY, *self.LOCATION) as location:
            days = []
            # prints the daily summary for the first day of the week
            #print(location.daily.summary, end='\n---\n')
            # loops through the number of days in the week
            for day in location.hourly:
                # formats the weeks data into a dictionary for easy information access
                # day becomes the dictionary of the current date, the summary of the day
                # the min temp of the day and the max temp of the day
                day = dict(day=self.date.strftime(str(self.date)),
                           sum=day.summary,
                           temp=day.temperature
                           )
                # the dictionaries information is formatted and printed out to the user
                curr_temp = '{temp}'.format(**day).lower()
                curr_sum = '{sum}'.format(**day).lower()
                # increments the date by the timedelta
                self.date += self.timedelta(days=1)
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


def main(city, state):
    # imports the datetime library with the fields date and timedelta
    from datetime import date, timedelta

    # sets the date to today's date
    date = date.today()

    # gets the location from "zip_converter.py"
    LOCATION = zip_converter.main(city, state)

    # creates a forcasts object from the forcasts class
    forcast = forcasts(LOCATION, date, timedelta)

    temperature, summary = forcast.weeklyForcast()

    return temperature, summary
