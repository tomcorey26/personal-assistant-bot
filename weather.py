from darksky import forecast
import zip_converter
from api_keys import *


class Forecasts:

    # class constructor to get values
    def __init__(self, lat, lng, date, timedelta):
        self.coorinatePoints = lat, lng
        self.date = date.today()
        self.timedelta = timedelta
        self.location = forecast(DARK_SKY_KEY, *self.coorinatePoints)


    # method to take in the location, date, and timedelta and will put back the weekly forecast, aka 7 day forecast
    def hourlyForecast(self):
        
        # formats the weeks data into a dictionary for easy information access
        # Hour becomes the dictionary of the current date, the summary of the hour
        hour = dict(hour=self.date.strftime(str(self.date)),
                    #each dictionary key corresponds to the data taken from the DarkSky API.
                    sum=self.getCurrentSummary(), #summarry of weather for the hour
                    temp=self.getTemperature(), #the temperature at the current time
                    dewpoint = self.getDewPoint(), #the current dewpoint
                    humid = self.getHumidity(), #the current humidity
                    wind = self.getWindSpeed(), #the current wind speed
                    windBearing = self.getWindBearing(), #the direction that the wind is blowing in (36o degrees)
                    pressure = self.getPressure(), #the pressure in mm HG
                    ozone = self.getOzone(), #the current ozone level
                    precipitation = self.getPrecipitation(), #the likelyhood it will rain
                    icon = self.getIcon()
                    )            
        #formats the information in the dictionary keys and sets them to variables
        curr_temp = '{temp}'.format(**hour).lower()
        curr_sum = '{sum}'.format(**hour).lower()
        curr_dew = '{dewpoint}'.format(**hour).lower()
        curr_humid = '{humid}'.format(**hour).lower()
        curr_wind = '{wind}'.format(**hour).lower()
        curr_windBearing = '{windBearing}'.format(**hour).lower()
        curr_pressure = '{pressure}'.format(**hour).lower()
        curr_ozone = '{ozone}'.format(**hour).lower()
        curr_icon = '{icon}'.format(**hour).lower()

        #returns the data back for use.
        return curr_temp, curr_sum, curr_dew, curr_humid, curr_wind, curr_windBearing, curr_pressure, curr_ozone, curr_icon


    #this method will supply data with 4 hour intervals, it will supply the weather and certain important metrics on a 4 hour basis.
    def dailyIntervals(self):
        #takes the data and puts it into a dictionary
        curr_temps = []
        curr_humids = []
        curr_winds = []
        curr_windBearings = []
        curr_precipitations = []
        
        for i in range(0,24,4):
            day = dict(day = self.date.strftime(str(self.date)),
                        #each of the hourly tags have list indexes as it will be returning the 4 hour loop of information, the next value will be 3 6 9 and so on 
                        temp=self.location.hourly[i].temperature,
                        humid = self.location.hourly[i].humidity,
                        wind = self.location.hourly[i].windSpeed,
                        windBearing = self.location.hourly[i].windBearing,
                        precipitation = self.location.hourly[i].precipProbability
                        )
            #sets variables of formated text from the dictionary
            curr_temp = '{temp}'.format(**day).lower()
            curr_humid = '{humid}'.format(**day).lower()
            curr_wind = '{wind}'.format(**day).lower()
            curr_windBearing = '{windBearing}'.format(**day).lower()
            curr_precipitation = '{precipitation}'.format(**day).lower()

            curr_temps.append(curr_temp)
            curr_humids.append(curr_humid)
            curr_winds.append(curr_wind)
            curr_windBearings.append(curr_windBearing)
            curr_precipitations.append(curr_precipitation)



        #sends the data back for use.
        return curr_temps, curr_humids, curr_winds, curr_windBearings, curr_precipitations
    
    #gives the summary of the weeks weather
    #it will print out the information for each day including the minimum temp, max temp the summary and the precipitation percentage.
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
        return self.coorinatePoints

    # returns the date we are currently concerned with
    def getDate(self):
        return self.date

    # returns the timedelta we are currently concerned with
    def getTimeDelta(self):
        return self.timedelta

    #these functions are here so that if someone wants just a single aspect of the weahter
    #they will be able to request it through the chat bot window.
    #it is unlikely that the feature will be implemented via the GUI.
    #returns the current temperature
    def getTemperature(self):
        return self.location.currently.temperature
    
    #returns the current humidity
    def getHumidity(self):
        return self.location.currently.humidity

    #returns the current precipitation
    def getPrecipitation(self):
        return self.location.currently.precipProbability

    #returns the current wind speed
    def getWindSpeed(self):
        return self.location.currently.windSpeed

    #gets the bearing of the wind
    def getWindBearing(self):
        return self.location.currently.windBearing
    
    #returns the current weather summary
    def getCurrentSummary(self):
        return self.location.currently.summary

    #returns the current ozone level
    def getOzone(self):
        return self.location.currently.ozone

    #returns the current dewpoint 
    def getDewPoint(self):
        return self.location.currently.dewPoint

    #returns the icon for the current weather conditions
    def getIcon(self):
        return self.location.currently.icon

    #returns the pressure in mm hg
    def getPressure(self):
        return self.location.currently.pressure
    

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

    # creates a forecasts object from the forecasts class
    forecast = Forecasts(lat, lng, date, timedelta)
    temperature, summary, dewPoint, humidity, wind, windBearing, pressure, ozone, icon = forecast.hourlyForecast()
    temps, humids, winds, bearings, precips = forecast.dailyIntervals()

    #this is a possible format for printing out the text of the intervals.
    #for i in range(len(temps)):
    #    print(temps[i] + " " + humids[i] +  " " + winds[i] + " " +  bearings[i] +  " " + precips[i])

    return temperature, summary

