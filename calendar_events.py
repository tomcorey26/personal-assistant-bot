#Calendar Apllication
import json
import os.path
from datetime import datetime
from command_output import say
from input_converter import myCommand

#define an variable to check for user input
input_type = "speech"

#check if the calendar json exists
def appCheck():
    #check if the file exists
    if os.path.isfile("calendar.json"):
        print("Json file found")
        return
    #if not, create it
    else:
        data = open("calendar.json", "w+")
        events = {}
        with data as outfile:
            json.dump(events, outfile)
        data.close()
        print("Json file created")

#Retrieve json information and return it as a dictionary
def get_data():
    file_name = "calendar.json"
    if os.path.isfile(file_name):
        # print("Json file found")
        with open(file_name) as json_file:
            data = json.load(json_file)
            return data
    else:
        data = open("calendar.json", "w+")
        with data as outfile:
            json.dump("{}", outfile)
        data.close()

#Write dictionary to json file
def write_data(user_data):
    data = open("calendar.json","w+")

    with data as outfile:
        json.dump(user_data,outfile)
    data.close()

def convert_date(date):
    from dateutil.parser import parse
    d = parse(date)
    date = str(d.strftime("%m"))+ "-" + str(d.strftime("%d")) + "-" + str(d.strftime("%y"))
    return date

#Adds an event to json file dicitonay and writes it
def addEvent():
    x = get_data()
    #if using speech for input
    if input_type == "speech":
        say("Event Name: ")
        eventName = myCommand().lower()
        say("Event Time: ")
        eventTime = myCommand().lower()
        say("Event Date: ")
        eventDate = myCommand().lower()
    #otherwise, use text-based input
    else:
        eventName = input("Event Name: ").lower()
        eventTime = input("Event Time (ex 12:00 p.m.): ").lower()
        eventDate = input("Event Date (ex 12-1-19): ").lower()
    #convert the date for simplicity
    eventDate = convert_date(eventDate)
    #add this criteria to a dictionary
    x[eventName] = []
    x[eventName].append({
        'Event Name':eventName,
        'Event Time':eventTime,
        'Event Date':eventDate
    })
    #add the event to the calendar
    write_data(x)
    return str(x[eventName]) + " has been added to your calendar"

#Finds a specific event based off name, time, or date
def findEvent(name):
    name = name.lower()
    x = get_data()
    for event, eventInfo in x.items():
        if event == name:
            return "Here is your event info: \n" + str(x[name])
        for i in range(len(eventInfo)):
            if eventInfo[i]["Event Time"] == name:
                return "Event found with " + name + ": \n" + str(eventInfo[i])
            elif eventInfo[i]["Event Date"] == convert_date(name):
                return "Event found with " + name + ": \n" + str(eventInfo[i])
    return "Event not found with given criteria"

#Removes a specific event by name
def removeEvent(name):
    name = name.lower()
    x = get_data()
    print("Removing " + str(x[name]) + " from your calendar")
    del x[name]
    write_data(x)

#Prints all events in a more elegant form instead of dictionary stucture
def printCal():
    x = get_data()
    for event, eventInfo in x.items():
        say("Event: " + str(event))
        for i in range(len(eventInfo)):
            print("Event Time: ",eventInfo[i]["Event Time"])
            print("Event Date: ",eventInfo[i]["Event Date"])
            print("--------------------")

#Do specific actions based on choice
def choices(choice):
    #check for the calendar file
    appCheck()
    #view
    if "view" in choice:
        printCal()
        return "Here are your events"
    #add
    elif "add" in choice:
        return addEvent()
    #search
    elif "search" in choice:
        # if using speech for input
        if input_type == "speech":
            say("Event Criteria (name, time, or date): ")
            name = myCommand()
        #if using text box for input
        else:
            name = input("Enter your event criteria (name, time, or date): ")
        #find the event with the input given
        return findEvent(name)
    #remove
    elif "remove" in choice:
        # if using speech for input
        if input_type == "speech":
            say("Event Title: ")
            name = myCommand()
        #if using text box for input
        else:
            name = input("Enter your event title: ")
        #remove the given event
        removeEvent(name)
        return name + " successfully removed!"