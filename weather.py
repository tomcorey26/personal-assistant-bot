from api_keys import *
from darksky import forecast
from datetime import date, timedelta
from coords_to_zip import *

LOCATION = latitude, longitude

date = date.today()

with forecast(DARK_SKY_KEY, *LOCATION) as location:
    print(location.daily.summary, end='\n---\n')
    for day in location.daily:
        day = dict(day=date.strftime(str(date)),
                   sum=day.summary,
                   tempMin=day.temperatureMin,
                   tempMax=day.temperatureMax
                   )

        print('{day}: {sum} Temp range: {tempMin} - {tempMax}'.format(**day))
        date += timedelta(days=1)



