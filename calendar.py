import json
import os.path

#Checks if calendar file exists. If not, create it
def appCheck():
    if os.path.isfile("calendar.json") == True:
        print("Json file found")
        return
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
    with open(file_name) as json_file:
        data = json.load(json_file)
        return data


#Write dictionary to json file
def write_data(user_data):
    data = open("calendar.json","w+")

    with data as outfile:
        json.dump(user_data,outfile)
    data.close()


#Adds an event to json file dicitonay and writes it
def addEvent():
    x = get_data()
    eventName = input("Event Name: ").lower()
    eventTime = input("Event Time (ex 12:00pm): ").lower()
    eventDate = input("Event Date (ex 12-1-19): ").lower()
    x[eventName] = []
    x[eventName].append({
        'Event Name':eventName,
        'Event Time':eventTime,
        'Event Date':eventDate
    })
    write_data(x)
    print(x[eventName]," has been added to your calendar")

#Finds a sepcific event based off name, time, or date
def findEvent(name):
    name = name.lower()
    x =get_data()
    for event, eventInfo in x.items():
        if event == name:
            print("Here is your event info")
            print(x[name])
            return
        for i in range(len(eventInfo)):
            if eventInfo[i]["Event Time"] == name:
                print("Event found with ",name)
                print(eventInfo[i])
                return
            elif eventInfo[i]["Event Date"] == name:
                print("Event found with ", name)
                print(eventInfo[i])
                return
    print("Event not found with given criteria")
    return


#Removes a specific event by name
def removeEvent(name):
    name = name.lower()
    x = get_data()
    print("Removing ",x[name]," from your calendar")
    del x[name]
    write_data(x)

#Simple UI for testing purposes
def main():
    appCheck()
    check = True
    print("1: View data. 2: Add event. 3: Search an event. 4: Remove an event. 5: End")
    while check:
        choice = input("Choice: ")
        if choice == "1":
            x = get_data()
            print(x)
        elif choice == "2":
            addEvent()
        elif choice == "3":
            name = input("Enter your event title: ")
            findEvent(name)
        elif choice == "4":
            name = input("Enter your event title: ")
            removeEvent(name)
        else:
            print("End")
            return



main()