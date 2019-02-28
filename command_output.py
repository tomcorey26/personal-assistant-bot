import pyttsx3
from datetime import datetime
import time
import input_converter

#speaks text back to the user
def say(response):
    print(response)
    engine = pyttsx3.init()
    engine.say(response)
    engine.setProperty('rate',120)  #120 words per minute
    engine.setProperty('volume',0.9) #90% volume
    engine.runAndWait() #Run voice and wait for it to finish
    return engine

#function to order a pizza
def order_pizza():
    import pizzapi
    #prompt the user with their order
    say("Ok, what would you like to order?")
    # get user data for command use
    import setup
    user_data = setup.get_data()
    # get user's information from user file
    user_data["email"] = input("Email: ").lower()
    user_data["phone"] = input("Phone Number(Ex: 1234567890): ").lower()
    user_data["address"] = input("Address: ").lower()
    setup.write_data(user_data)
    customer = pizzapi.Customer(user_data["first_name"], user_data["last_name"], user_data["email"], user_data["phone"])
    address = pizzapi.Address(user_data["address"], user_data["city"], user_data["state"], user_data["zip"])
    store = address.closest_store()
    pizza_order(store, customer, address)
    order_list = input_converter.myCommand()
    return "Ok, I will order your " + order_list

#function to look for a recipe
def get_recipe():
    # get the food that is being requested
    food = input[command_input.index("recipe") + 1]
    # find the requested recipe
    return "Here's a recipe for " + food + ": " + "recipe(food)"

#function to current system time
def get_time():
    # get substring from system datetime
    time = (str(datetime.now().time())[0:5])
    # convert to 24-hour format object
    time_24 = time.strptime(time, "%H:%M")
    # convert that to 12-hour format
    time_12 = time.strftime("%I:%M %p", time_24)
    return "It is currently " + time_12

#function to find out the weather
def get_weather(command_input):
    # get user data for command use
    import setup
    user_data = setup.get_data()
    # figure out the location to detect the weather
    try:
        # if a location is given, use that
        location = command_input[command_input.index("weather") + 1]
        # print("location: ", location)
        # separate city and state into individual strings
        state_list = ["al", "ak", "az", "ar", "ca", "co", "ct", "dc", "de", "fl",
                      "ga", "hi", "id", "il", "in", "ia", "ks", "ky", "la", "me",
                      "md", "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh",
                      "nj", "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri",
                      "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy"]
        # print("sub: ",location[-3:])
        for s in state_list:
            if (" " + s) in location[-3:]:
                state = s
                city = location.replace((" " + state), "")
                # print("city: ", city, "state: ", state)
    except IndexError:
        city = user_data["city"]
        state = user_data["state"]
        location = city + " " + state
    # find the conditions in that location
    import weather
    try:
        temp, summ = weather.main(city, state)
        # construct a single output string from this input
        return "In " + location + ", it is currently " + temp + " degrees and " + summ + "."
    except:
        return "Cannot connect to weather service."

def tell_joke():
    from random import randint
    joke_list = ["Your social life.", "Something about a cow.", "Your mom."]
    joke = joke_list[randint(0,len(joke_list)-1)]
    return joke

#do different actions based on the given input
def commands(command_input):
    #find which command to execute based on user input
    key = ""
    for word in command_input:
        if "settings" in word:
            key = "settings"
        if ("domino's" in word) or ("pizza" in word):
            key = "pizza";
        elif "recipe" in word:
            key = "recipe"
        elif "time" in word:
            key = "time"
        elif "weather" in word:
            key = "weather"
        elif "joke" in word:
            key = "joke"

    #define an output variable for later
    output = "Invalid Command."
    
    ##Commands
    #access the settings
    if "settings" in key:
        from setup import settings
        output = str(settings())
    #order a pizza
    elif "pizza" in key:
        output = order_pizza()
    #look for a recipe
    elif "recipe" in key:
        output = get_recipe()
    #current system time
    elif "time" in key:
        output = get_time()
    #find out the weather
    elif "weather" in key:
        output = get_weather(command_input)
    #tell a joke
    elif "joke" in key:
        output = tell_joke()

    say(output)
