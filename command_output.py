import pyttsx3
from datetime import datetime
import time
import input_converter
import nltk

#speaks text back to the user
def say(response):
    print(response)
    engine = pyttsx3.init()
    engine.say(response)
    engine.setProperty('rate',120)  #120 words per minute
    engine.setProperty('volume',0.9) #90% volume
    engine.runAndWait() #Run voice and wait for it to finish
    return engine

#function to tell some jokes
def tell_joke():
    from random import randint
    joke_list = ["Your social life.", "Something about a cow.", "Your mom."]
    joke = joke_list[randint(0,len(joke_list)-1)]
    return joke

#function to catch a fish
def catch_fish():
    import fish
    result = fish.main()
    return result

#function to order a pizza
def order_pizza():
    import init_order
    #go through the order process
    return init_order.main()

#function to scrape for a recipe
def get_recipe(command_input):
    import recipe_finder
    #get the food that is being requested
    try:
        food = command_input[command_input.index("recipe") + 1]
    except IndexError:
        food = command_input[command_input.index("recipe") - 1]
    try:
        #call the recipe finder
        ingredients = recipe_finder.main(food)
    except ValueError:
        #there is not a recipe listed for this food
        return "Not specific enough"
    #get the recipe back to the user
    return "Here's a recipe for " + food + ": \n " + str(ingredients)

#function to current system time
def get_time():
    # get substring from system datetime
    time_str = (str(datetime.now().time())[0:5])
    # convert to 24-hour format object
    time_24 = time.strptime(time_str, "%H:%M")
    # convert that to 12-hour format
    time_12 = time.strftime("%I:%M %p", time_24)
    return "It is currently " + time_12

#function to find out the weather
def get_weather(command_input):
    import setup
    import zip_converter
    # get user data for command use
    user_data = setup.get_data()
    # create base variables to be modified later
    city = ""
    state = ""
    #figure out the location to detect the weather
    try:
        # if a location is given, use that
        location = command_input[command_input.index("weather") + 1]
        print("Location: ", location)
        #if a zip code is given
        try:
            print(int(location))
            city, state = zip_converter.zip_to_city_state(location)
        #if a city and state are given
        except ValueError:
            # separate city and state into individual strings
            state_list = ["al", "ak", "az", "ar", "ca", "co", "ct", "dc", "de", "fl",
                          "ga", "hi", "id", "il", "in", "ia", "ks", "ky", "la", "me",
                          "md", "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh",
                          "nj", "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri",
                          "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy"]

            state_name_list = ["alabama","alaska","arizona","arkansas","california",
                               "colorado","connecticut","delaware","florida","georgia",
                               "hawaii","idaho","illinois","indiana","iowa",
                               "kansas","kentucky","louisiana","maine","maryland",
                                "massachusetts","michigan","minnesota","mississippi","missouri",
                               "montana","nebraska","nevada","new hampshire","new jersey",
                               "new mexico","new york","north carolina","north dakota","ohio",
                               "oklahoma","oregon","pennsylvania","rhode island","south carolina",
                               "south dakota","tennessee","texas","utah","vermont",
                               "virginia","washington","west virginia","wisconsin","wyoming"]

            #find out what sort of location we're dealing with
            loc = ""
            #find state abbreviations in location string
            for s in state_list:
                if (" " + s) in location[-3:]:
                    #isolate the state into a variable
                    state = s
                    #isolate the city into a variable
                    city = location.replace((" " + state), "")
                    loc = "abb"
            #find the state names in location string
            for s in state_name_list:
                if (" " + s) in location:
                    #isolate the state into a variable
                    state = s
                    #isolate the city into a variable
                    city = location.replace((" " + state), "")
                    loc = "name"
            if loc == "":
                city, state = zip_converter.city_to_city_state(location)



    #if no location is given
    except IndexError:
        #use user information
        city = user_data["city"]
        state = user_data["state"]
        location = city + " " + state

    #get latitude and longitude from city and state
    latitude, longitude = zip_converter.main(city, state)
    # find the conditions in that location
    import weather
    print("")
    temp, summ = weather.main(latitude, longitude)
    # construct a single output string from this input
    return "In " + city + " " + state + ", it is currently " + temp + " degrees and " + summ + "."

#function to search top reddit posts
def reddit_posts(command_input):
    import RedditApi
    #pull the subreddit from the input
    sub = ""
    for token in command_input:
        #if a sub is given
        if "r /" in token or "/" in token:
            sub = token
        elif "reddit" in token or "all" in token:
            sub = "all"
    #pull the subreddit string together to form the proper name
    #fix underscores
    sub = sub.replace("underscore", "_")
    #remove whitespace
    sub = sub.replace(" ", "")
    #remove r/
    sub = sub.replace("r/", "")
    print("sub: ",sub)
    say("Here are the top posts from r/" + sub + ":\n")
    output = RedditApi.redditPosts(5, sub)
    #format the string to make it look nicer
    result = ""
    for key, value in output.items():
        result += key + ":\n" + value + "\n\n"
    print(result)
    #return the final string result
    return result

#function to utilize the calendar
def get_calendar(command_input):
    import calendar_events
    if "view" in command_input:
        choice = "view"
    elif "add" in command_input:
        choice = "add"
    elif "remove" in command_input:
        choice = "remove"
    elif "search" in command_input or "find" in command_input:
        choice = "search"
    #perform a different calendar action based on the choice given
    return calendar_events.choices(choice)

#function to get directions to a location
def get_directions(command_input):
    import directions
    destination = ""
    if " to " in command_input:
        destination = command_input[command_input.index(" to ")+4:]
    print("Location: ", destination)
    dir_text = directions.locate(destination)
    return dir_text

#do different actions based on the given input
def commands(command_input):
    #find which command to execute based on user input
    key = ""
    if "settings" in command_input:
        key = "settings"
    if any(c in command_input for c in ("pizza", "domino's")) and not ("recipe" in command_input):
        key = "pizza";
    elif "recipe" in command_input:
        key = "recipe"
    elif "time" in command_input:
        key = "time"
    elif "weather" in command_input:
        key = "weather"
    elif "joke" in command_input:
        key = "joke"
    elif any(c in command_input for c in ("fish", "catch", "cast", "snag")):
        key = "fish"
    elif "reddit" in command_input or "posts" in command_input:
        key = "reddit"
    elif any(c in command_input for c in ("add", "remove", "search", "find", "view")) and any(d in command_input for d in ("event", "calendar")):
        key = "calendar"
    elif any(c in command_input for c in ("directions", "route", "direct", "locate")):
        key = "directions"

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
        #parse the text for this feature
        parsed_command = input_converter.convert_text(command_input.lower())
        #use the parsed text to get the desired output
        output = get_recipe(parsed_command)
    #current system time
    elif "time" in key:
        output = get_time()
    #find out the weather
    elif "weather" in key:
        #parse the text for this feature
        parsed_command = input_converter.convert_text(command_input.lower())
        #use the parsed text to get the desired output
        output = get_weather(parsed_command)
    #tell a joke
    elif "joke" in key:
        output = tell_joke()
    #catch a fish
    elif "fish" in key:
        output = catch_fish()
    #access top reddit posts
    elif "reddit" in key:
        #parse the text for this feature
        parsed_command = input_converter.convert_text(command_input.lower())
        #use the parsed text to get the desired output
        output = reddit_posts(parsed_command)
    #manipulate or view calendar events
    elif "calendar" in key:
        output = get_calendar(command_input)
    elif "directions" in key:
        output = get_directions(command_input)

    return output