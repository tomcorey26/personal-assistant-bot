import pyttsx3
from datetime import datetime
import time

def say(response):
    print(response)
    engine = pyttsx3.init()
    engine.say(response)
    engine.setProperty('rate',120)  #120 words per minute
    engine.setProperty('volume',0.9) #90% volume
    engine.runAndWait() #Run voice and wait for it to finish
    return engine

def commands(input):
    print("given input: ", input)
    #find, based on the input, which command to execute
    key = ""
    for word in input:
        if "recipe" in word:
            key = "recipe"
        elif "time" in word:
            key = "time"
        elif "weather" in word:
            key = "weather"
        elif "joke" in word:
            key = "joke"
    print(key)

    #define an output variable for later
    output = "Invalid Command."
    
    ##Commands
    #look for a recipe
    if "recipe" in key:
        #get the food that is being requested
        food = input[input.index("recipe")+1]
        #find the requested recipe
        output = "Here's a recipe for " + food + ": " + "recipe(food)"
    #current system time
    elif "time" in key:
        #get substring from system datetime
        time = (str(datetime.now().time())[0:5])
        #convert to 24-hour format object
        time_24 = time.strptime(time, "%H:%M")
        #convert that to 12-hour format
        time_12 = time.strftime("%I:%M %p", time_24)
        output = "It is currently " + time_12
    #find out the weather
    elif "weather" in key:
        #figure out the location to detect the weather
        location = input[input.index("weather")+1]
        #find the conditions in that location
        conditions = "weather(location)"
        #construct a single output string from this input
        output = "In " + location + ", it is currently " + str("weather(location)")
    #tell a joke
    elif "joke" in key:
        output = "Your social life."
        #jokes()

    say(output)
