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
    order_list = input_converter.myCommand()
    return "Ok, I will order your " + order_list

#function to scrape for a recipe
def get_recipe(command_input):
    from recipe_scrapers import scrape_me
    #get the food that is being requested
    try:
        food = command_input[command_input.index("recipe") + 1]
    except IndexError:
        food = command_input[command_input.index("recipe") - 1]
    #google a recipe from allrecipes.com
    from googlesearch import search
    query = food + " allrecipes.com"
    #find the desired url
    url = ""
    for i in search(query, tld="com", num=1, stop=1, pause=2):
        url = i
    print("url: ", url)
    #assign scraper to this url
    scraper = scrape_me(url)
    #find the ingredients for the recipe and convert that into a string
    ingredients = str(scraper.ingredients())
    #remove brackets and add line breaks in the string to make it more readable
    ingredients = ingredients.replace(",", "\n")
    ingredients = ingredients.replace("[", "")
    ingredients = ingredients.replace("]", "")
    ingredients = ingredients.replace("'", "")
    #get the recipe back to the user
    return "Here's a recipe for " + food + ": \n " + str(ingredients)

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
        output = get_recipe(command_input)
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
