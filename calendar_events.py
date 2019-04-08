import json
import os.path

#Check if the calendar json exists
def appCheck():
    if os.path.isfile("calendar.json"):
        print("Json file found")
        return
    else:
        data = open("calendar.json","w+")
        events = {}
        with data as outfile:
            json.dump(events,outfile)
        data.close()
        print("Json file created")

#Retrieve Json information and return it as a dictionary
def getData():
    fileName = "calendar.json"
    if os.path.isfile(fileName):
        with open(fileName) as jsonFile:
            data = json.load(jsonFile)
            return data
    else:
        return "Could not find Json file"
    data.close()


#Write dictionary to json file
def writeData(calendarData):
    data = open("calendar.json","w+")

    with data as outfile:
        json.dump(calendarData,outfile)
    data.close()

#Converts date from "mm/dd/yy" to [d,m,yyy]
def convertDate(date):
    from dateutil.parser import parse
    d = parse(date)
    date = str(d.strftime("%m")) + "/" + str(d.strftime("%d")) + "/" + str(d.strftime("%y"))
    date_array = [int(d.strftime("%d")), int(d.strftime("%m")), int(d.strftime("%Y"))]
    return date_array


#Adds an event to json file and writes it
def addEvent(date,time,name):
    x = getData()
    dateArr = convertDate(date)
    eventTime = str(time).lower()
    eventName = str(name).lower()

    x[date] = []
    x[date].append({"Event Name":eventName,
                    "Event Date": date,
                    "Event Time": eventTime,
                    "Event Arr": dateArr
                    })
    writeData(x)

    return eventName, "has been added to your calendar"

#Finds an event using dateArr as paramenter or dateStr
def findEvent(calEvent):
    x = getData()
    if isinstance(calEvent,list) == True:
        for event, eventInfo in x.items():
            for i in range(len(eventInfo)):
                print(eventInfo[i]["Event Arr"])
                if eventInfo[i]["Event Arr"] == calEvent:
                    print("Event found for",event+":", eventInfo[i]["Event Name"], "at", eventInfo[i]["Event Time"])
                    return

    else:
        calEvent = str(calEvent).lower()
        for event, eventInfo in x.items():
            for i in range(len(eventInfo)):
                if eventInfo[i]["Event Name"] == calEvent:
                    print("Event found for", eventInfo[i]["Event Name"]+":", event,"at",eventInfo[i]["Event Time"])
                    return
    print("Event could not be found")
    return

#TODO Finish this function to remove an event
def removeEvent(name):
    name = name.lower()
    x = getData()
    print("Removing " + str(x[name]) + " from your calendar")
    del x[name]
    writeData(x)

appCheck()

