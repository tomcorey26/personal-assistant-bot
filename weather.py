from darksky import forecast
import zip_converter
from api_keys import *


class forecasts:

    # class constructor to get values
    def __init__(self, lat, lng, date, timedelta):
        self.LOCATION = lat, lng
        self.date = date.today()
        self.timedelta = timedelta
        self.location = forecast(DARK_SKY_KEY, *self.LOCATION)


    # method to take in the location, date, and timedelta and will put back the weekly forcast, aka 7 day forcast
    def hourlyForcast(self):
        # calls the darksky api giving it the location(latitude and longitude) and the api key
        # formats the weeks data into a dictionary for easy information access
        # day becomes the dictionary of the current date, the summary of the day
        # the min temp of the day and the max temp of the day
        hour = dict(hour=self.date.strftime(str(self.date)),
                    sum=self.location.summary,
                    temp=self.location.temperature,
                    dewpoint = self.location.dewPoint,
                    humid = self.location.humidity,
                    wind = self.location.windSpeed,
                    windBearing = self.location.windBearing,
                    pressure = self.location.pressure,
                    ozone = self.location.ozone,
                    precipitation = self.location.precipProbability
                    )
            # the dictionaries information is formatted and printed out to the user
        curr_temp = '{temp}'.format(**hour).lower()
        curr_sum = '{sum}'.format(**hour).lower()
        curr_dew = '{dewpoint}'.format(**hour).lower()
        curr_humid = '{humid}'.format(**hour).lower()
        curr_wind = '{wind}'.format(**hour).lower()
        curr_windBearing = '{windBearing}'.format(**hour).lower()
        curr_pressure = '{pressure}'.format(**hour).lower()
        curr_ozone = '{ozone}'.format(**hour).lower()

            # increments the date by the timedelta
        return curr_temp, curr_sum, curr_dew, curr_humid, curr_wind, curr_windBearing, curr_pressure, curr_ozone

    def dailyIntervals(self):

        day = dict(day = self.date.strftime(str(self.date)),
                    temp=self.location.hourly[0].temperature,
                    humid = self.location.hourly[0].humidity,
                    wind = self.location.hourly[0].windSpeed,
                    windBearing = self.location.hourly[0].windBearing,
                    precipitation = self.location.hourly[0].precipProbability
                    )
        curr_temp = '{temp}'.format(**day).lower()
        curr_humid = '{humid}'.format(**day).lower()
        curr_wind = '{wind}'.format(**day).lower()
        curr_windBearing = '{windBearing}'.format(**day).lower()
        curr_precipitation = '{precipitation}'.format(**day).lower()

        return curr_temp, curr_humid, curr_wind, curr_windBearing, curr_precipitation
    

    def weeklySummary(self):

        weekday = self.date.today()
        print(self.location.daily.summary, end='\n---\n')
        for day in self.location.daily:
            day = dict(day =self.date.strftime(str(weekday)),
                    sum = day.summary,
                    precipitation = self.location.precipProbability,
                    tempMin = day.temperatureMin,
                    tempMax = day.temperatureMax
                    )
            print('{day}: {sum} Temp range: {tempMin} - {tempMax}, Precipitation Chance : {precipitation}'.format(**day))
            weekday += self.timedelta(days=1)


    # returns the location we are currently concerned with
    def getLocation(self):
        return self.LOCATION

    # returns the date we are currently concerned with
    def getDate(self):
        return self.date

    # returns the timedelta we are currently concerned with
    def getTimeDelta(self):
        return self.timedelta


def main(lat, lng):
    # imports the datetime library with the fields date and timedelta
    from datetime import date, timedelta

    # sets the date to today's date
    date = date.today()

    # creates a forcasts object from the forcasts class
    forecast = forecasts(lat, lng, date, timedelta)

    temperature, summary, dewPoint, humidity, wind, windBearing, pressure, ozone = forecast.hourlyForcast()

    forecast.dailyIntervals()
    forecast.weeklySummary()

    return temperature, summary

print(main(41.4476, -71.5247))