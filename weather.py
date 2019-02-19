from api_keys import *
from darksky import forecast
from coords_to_zip import *

class forcasts():
    
    #class constructor to get values
    def __init__(self, LOCATION, date, timedelta):
        self.LOCATION = LOCATION
        self.date = date
        self.timedelta = timedelta

    #method to take in the location, date, and timedelta and will put back the weekly forcast, aka 7 day forcast
    def weeklyForcast(self):

        #calls the darksky api giving it the location(latitude and longitude) and the api key
        with forecast(DARK_SKY_KEY, *self.LOCATION) as location:
            #prints the daily summary for the first day of the week
            print(location.daily.summary, end='\n---\n')
            #loops through the number of days in the week
            for day in location.daily:
                #formats the weeks data into a dictionary for easy information access
                #day becomes the dictionary of the current date, the summary of the day
                #the min temp of the day and the max temp of the day
                day = dict(day=self.date.strftime(str(self.date)),
                        sum=day.summary,
                        tempMin=day.temperatureMin,
                        tempMax=day.temperatureMax
                        )
                #the dictionaries information is formatted and printed out to the user
                print('{day}: {sum} Temp range: {tempMin} - {tempMax}'.format(**day))
                #increments the date by the timedelta
                self.date += self.timedelta(days=1)

    #returns the location we are currently concerned with
    def getLocation(self):
        return self.LOCATION

    #returns the date we are currently concerned with
    def getDate(self):
        return self.date

    #returns the timedelta we are currently concerned with
    def getTimeDelta(self):
        return self.timedelta


def main():
    #imports the datetime library with the fields date and timedelta
    from datetime import date, timedelta

    #sets the date to todays date
    date=date.today()

    #gets the location from "coords_to_zip.py"
    LOCATION = latitude, longitude

    #creates a forcasts object from the forcasts class
    forcast = forcasts(LOCATION, date, timedelta)

    forcast.weeklyForcast()

main()

