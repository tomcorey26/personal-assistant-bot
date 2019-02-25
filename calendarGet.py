import calendar





def addEvent(month,day,event):
    calendar.months[month][day].append(event)
    print("You have added", event, "to", month, day)


def getEvent(month,day):
    print("Here is what your schedule is for", month, day,":")
    if not calendar.months[month][day]:
        print("You have no events that day")
    else:
        for i in range(len(calendar.months[month][day])):
            print(calendar.months[month][day][i])



def main():
    event0 = "Lunch with friends"
    event1 = "Homework"
    event2 = "Dinner with parents"

    addEvent("january", 3, event0)
    addEvent("january",3,event1)
    addEvent("january", 10, event2)

    print("\n")

    getEvent("january", 3)

    print("\n")
    getEvent("january",10)




main()