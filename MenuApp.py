#disable multitouch functionality
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

#import the required kivy dependencies
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from datepicker import CalendarWidget
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from functools import partial
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.image import Image

#import all of the local python files that the group created
import time

#imports for fish file
from fish import Fish
import random
import calendar_events as events
import RedditApi

#weather import statements
import weather
from datetime import date, timedelta
import location_to_coords

from front_order import *
import input_converter
import recipe_finder
import zip_converter
import setup
import TwitterApi
import command_output
import directions
import News

#Twitter/Reddit error handling
import tweepy
import prawcore

Builder.load_file('menubar.kv')
Builder.load_file('chatwindow.kv')
Builder.load_file('screens.kv')

class MenuContainer(AnchorLayout):

    #constructor
    def __init__(self, **kwargs):
        super(MenuContainer, self).__init__(**kwargs)

        #load the login popup when the app starts
        Clock.schedule_once(self.getStartupPopup, 0)

    def getStartupPopup(self, inst):
        pop = Popup(title='Welcome to SalmonBot!', title_align='center',content=Image(source='images/MainLogo.png'),
            size_hint=(None,None), height=400, width=400)
        pop.open()


class MenuManager(ScreenManager):

    #change the current screen to the one with the specified name
    def switchScreens(self, name):
        self.current = name

# TODO split these classes up into multiple different files, for readability
# where all of the screens functions can be stored.

class CalendarScreen(Screen):

    #a list of the currently toggled date. format = [day, month year]
    toggled_date =  ListProperty([0,0,0])

    #when the "date" property is changed, update the event label to reflect the events for the toggled date
    def on_toggled_date(self, instance, value):
        
        #if the toggled date is [0,0,0], print a default string
        if self.toggled_date == [0,0,0]:
            self.event_label.text = "Select a date to view/add an event"

        #if an actual date is selected, update the event label
        else:
            dateString = str(self.toggled_date[1]) + "-" + str(self.toggled_date[0]) + "-" + str(self.toggled_date[2])

            self.event_label.text = "events for " + dateString + "\n\n"
            self.event_label.text += events.findEvent(self.toggled_date)  

    def addEvent(self):

        #only open the popup if a date is selected
        if (self.toggled_date != [0,0,0]):

            #the functions in the AddEventPopup class will take
            #care of adding the event to the data file
            eventPopup = AddEventPopup(self)
            eventPopup.open()

    def removeEvents(self):
        #TODO remove an event (or all events on that day) from the data file
        return

class AddEventPopup(Popup):

    # takes a reference to the calendarScreen, so that the popup can easily
    # pass back the data
    def __init__(self, parent, **kwargs):
        super(AddEventPopup, self).__init__(**kwargs)

        #sets the parent CalendarScreen as an attribute of the popup
        #and get the selected date from the calendar screen
        self.parentScreen = parent
        self.date = parent.toggled_date
        self.event_label = parent.event_label

    def addEvent(self, time, name):

        #if either of the textInput boxes are empty, then display an error
        if time == '' or name == '':
            self.error_label.text = "error: please enter both a time and a name"
        else:

            #convert the date array into a string of mm/dd/yy
            dayString = str(self.date[0])
            monthString = str(self.date[1])
            yearString = str(self.date[2] % 100)
            if self.date[0] < 10:
                dayString = "0" + dayString
            if self.date[1] < 10:
                monthString = "0" + monthString

            dateString = monthString + "/" + dayString + "/" + yearString
            
            events.addEvent(dateString, self.time_input.text, self.name_input.text)

            #TODO update the calendar screen's event label
            self.event_label.text = "events for " + dateString + "\n\n"
            self.event_label.text += events.findEvent(self.date)

            #close the popup window
            self.dismiss()

    def __del__(self):
        print('popup was garbage collected')
        
    
class WeatherScreen(Screen):

    def getWeather(self):

        # save the string from the textbox and set the textbox to empty
        location = self.location_input.text
        self.location_input.text = ""

        # convert the location into latitude and longitude
        latitude, longitude, cityname = location_to_coords.main(location)

        # if the city isn't found, let the user know of the error
        if cityname == 'Unrecognized location':
            self.location_input.hint_text = "Error, location not found"
            self.location_input.hint_color = (1, .3, .3, 1)

        # otherwise, print out the current weather for that city
        else:

            # reset the userinput hint, in case they had an error before
            self.location_input.hint_text = "Enter ZIP code, city, or city/state"
            self.location_input.hint_color = (.2, .2, .2, 1)

            # display the name of the city
            self.city_label.text = f"Weather for {cityname}:"

            # display the city's weather
            ##  i have no idea: forecast = weather.Forecasts(lat, lng, date, timedelta)
            # i think what I should do is craft the main function to return each list of dictionaries.

            #  will use daily_forecast, hourly_forecast, current_conditions = weather.getCurrentget_weather(latitude, longitude)
            daily_forecast, hourly_forecast, current_conditions = weather.get_weather(latitude, longitude)
            """
            # temp, summ, icon, humid = weather.getCurrentget_weather(latitude, longitude)
            for i in daily_forecast:
                hey = ('{day}: {summary} Temp range: {tempMin} - {tempMax}'.format(**i))

            self.temp_button.text = hey
            """


            #temp, summ, icon, humid = weather.getCurrentget_weather(latitude, longitude)
            self.currently_button.text = "Current Conditions\n\n"\
                f"{current_conditions.get('temp')} °F\n" \
                f"(Feels like {current_conditions.get('feelsLike')} °F)\n" \
                f"{current_conditions.get('hourSummary')}\n" \
                f"{current_conditions.get('windBearing')} winds at " \
                f"{current_conditions.get('windSpeed')} mph\n" \
                f"{current_conditions.get('windGust')} mph gusts\n" \
                f"Visibility: {current_conditions.get('visibility')} miles\n" \
                f"UV Index: {current_conditions.get('uvIndex')}\n " \
                f"{current_conditions.get('cloudCover')}% cloud cover" \

            # Gets the weather icon from the weatherflaticons folder
            self.currently_button.background_normal = f"images\weatherflaticons\{current_conditions.get('icon')}.png"
            self.currently_button.background_down = f"images\weatherflaticons\{current_conditions.get('icon')}.png"

            self.hourly_button.halign = "left"
            self.hourly_button.font_size = 11
            self.hourly_button.text = f"                 Hourly Forecast\n\n" \
                f"{hourly_forecast[0].get('hour')}:00 {hourly_forecast[0].get('summary')}, {hourly_forecast[0].get('temp')}°F, {hourly_forecast[0].get('windSpeed')}mph {hourly_forecast[0].get('windBearing')}\n" \
                f"{hourly_forecast[1].get('hour')}:00 {hourly_forecast[1].get('summary')}, {hourly_forecast[1].get('temp')}°F, {hourly_forecast[1].get('windSpeed')}mph {hourly_forecast[1].get('windBearing')}\n" \
                f"{hourly_forecast[2].get('hour')}:00 {hourly_forecast[2].get('summary')}, {hourly_forecast[2].get('temp')}°F, {hourly_forecast[2].get('windSpeed')}mph {hourly_forecast[2].get('windBearing')}\n" \
                f"{hourly_forecast[3].get('hour')}:00 {hourly_forecast[3].get('summary')}, {hourly_forecast[3].get('temp')}°F, {hourly_forecast[3].get('windSpeed')}mph {hourly_forecast[3].get('windBearing')}\n" \
                f"{hourly_forecast[4].get('hour')}:00 {hourly_forecast[4].get('summary')}, {hourly_forecast[4].get('temp')}°F, {hourly_forecast[4].get('windSpeed')}mph {hourly_forecast[4].get('windBearing')}\n" \
                f"{hourly_forecast[5].get('hour')}:00 {hourly_forecast[5].get('summary')}, {hourly_forecast[5].get('temp')}°F, {hourly_forecast[5].get('windSpeed')}mph {hourly_forecast[5].get('windBearing')}\n" \
                f"{hourly_forecast[6].get('hour')}:00 {hourly_forecast[6].get('summary')}, {hourly_forecast[6].get('temp')}°F, {hourly_forecast[6].get('windSpeed')}mph {hourly_forecast[6].get('windBearing')}\n" \
                f"{hourly_forecast[7].get('hour')}:00 {hourly_forecast[7].get('summary')}, {hourly_forecast[7].get('temp')}°F, {hourly_forecast[7].get('windSpeed')}mph {hourly_forecast[7].get('windBearing')}\n" \
                f"{hourly_forecast[8].get('hour')}:00 {hourly_forecast[8].get('summary')}, {hourly_forecast[8].get('temp')}°F, {hourly_forecast[8].get('windSpeed')}mph {hourly_forecast[8].get('windBearing')}\n" \
                f"{hourly_forecast[9].get('hour')}:00 {hourly_forecast[9].get('summary')}, {hourly_forecast[9].get('temp')}°F, {hourly_forecast[9].get('windSpeed')}mph {hourly_forecast[9].get('windBearing')}\n" \
                f"{hourly_forecast[10].get('hour')}:00 {hourly_forecast[10].get('summary')}, {hourly_forecast[10].get('temp')}°F, {hourly_forecast[10].get('windSpeed')}mph {hourly_forecast[10].get('windBearing')}" \

            # Fills in the Weekly Forecast section
            self.daily_button.font_size = 11.5
            self.daily_button.text = f"Tomorrow: {daily_forecast[1].get('summary')}\n    High of {daily_forecast[1].get('tempHigh')}°F and low of {daily_forecast[1].get('tempLow')}°F.  Winds {daily_forecast[1].get('windBearing')} at {daily_forecast[1].get('windSpeed')} mph with gusts of {daily_forecast[1].get('windGust')} mph.\n" \
                f"{daily_forecast[2].get('day')}: {daily_forecast[2].get('summary')}\n    High of {daily_forecast[2].get('tempHigh')}°F and low of {daily_forecast[2].get('tempLow')}°F.  Winds {daily_forecast[2].get('windBearing')} at {daily_forecast[2].get('windSpeed')} mph with gusts of {daily_forecast[2].get('windGust')} mph.\n" \
                f"{daily_forecast[3].get('day')}: {daily_forecast[3].get('summary')}\n    High of {daily_forecast[3].get('tempHigh')}°F and low of {daily_forecast[3].get('tempLow')}°F.  Winds {daily_forecast[3].get('windBearing')} at {daily_forecast[3].get('windSpeed')} mph with gusts of {daily_forecast[3].get('windGust')} mph.\n" \
                f"{daily_forecast[4].get('day')}: {daily_forecast[4].get('summary')}\n    High of {daily_forecast[4].get('tempHigh')}°F and low of {daily_forecast[4].get('tempLow')}°F.  Winds {daily_forecast[4].get('windBearing')} at {daily_forecast[4].get('windSpeed')} mph with gusts of {daily_forecast[4].get('windGust')} mph.\n" \
                f"{daily_forecast[5].get('day')}: {daily_forecast[5].get('summary')}\n    High of {daily_forecast[5].get('tempHigh')}°F and low of {daily_forecast[5].get('tempLow')}°F.  Winds {daily_forecast[5].get('windBearing')} at {daily_forecast[5].get('windSpeed')} mph with gusts of {daily_forecast[5].get('windGust')} mph.\n" \
                f"{daily_forecast[6].get('day')}: {daily_forecast[6].get('summary')}\n    High of {daily_forecast[6].get('tempHigh')}°F and low of {daily_forecast[6].get('tempLow')}°F.  Winds {daily_forecast[6].get('windBearing')} at {daily_forecast[6].get('windSpeed')} mph with gusts of {daily_forecast[6].get('windGust')} mph.\n" \
                f"{daily_forecast[7].get('day')}: {daily_forecast[7].get('summary')}\n    High of {daily_forecast[7].get('tempHigh')}°F and low of {daily_forecast[7].get('tempLow')}°F.  Winds {daily_forecast[7].get('windBearing')} at {daily_forecast[7].get('windSpeed')} mph with gusts of {daily_forecast[7].get('windGust')} mph."

            # Include precipitation with {daily_forecast[1].get('precipProb')}% chance precipitation.

class TwitterScreen(Screen):

    def getTweets(self):
        
        user = self.twitter_input.text
        self.recent_tweets.text = "\n"

        #try/except handles user not found
        try:

            #Selected users last 5 tweets printed to gui
            twitter = TwitterApi.TwitterScrape(5, user)
            posts = twitter.grabRecentPosts()
            for status in posts:
                self.recent_tweets.text += user + ":\n" + status.text + "\n\n"

        except tweepy.error.TweepError:

            #Twitter user doesn't exist
            self.recent_tweets.text = "user not found"
        

class RedditScreen(Screen):

    def getPosts(self):

        #Try/except handles subreddit not found
        try:

            #Top 5 selected subeddit posts printed to gui
            posts = RedditApi.redditPosts(5, self.subreddit_input.text)
            self.top_posts.text = "\n"
            for (name, url) in posts.items():
                self.top_posts.text += (name + "\n" + url + "\n\n")
                
        except prawcore.exceptions.Redirect:

            #Subreddit not found- Redirected
            self.top_posts.text = "Subreddit not found"

        except prawcore.exceptions.NotFound:

            #Subreddit not found- 404 error
            self.top_posts.text = "Subreddit not found"

            

class FishScreen(Screen):

    # a list that holds the total amt of fish caught in a session
    # the tally only hold data for when the program is open
    fish_tally = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def castLine(self):

        #retrieve a fish object and get its species/wikipedia page
        num = random.randint(0,20)
        fish = Fish(num)
        catch = fish.castLine()
        species = catch.species
        wikiURL = catch.wiki_url
        fishID = catch.number

        #format the string for the screen's label
        if (species != "You fail to catch a fish"):
            species = "You caught a " + species
        self.ids._catch_label.text = species

        #dictionary of the image URL's
        #TODO find a better way to implement these
        fishImages = {1: "Trout.png", 2: "Salmon.png", 3:"Crayfish.png", 4:"Shark.png",
                      5: "Boots.png", 6: "Lobster.png", 7: "Sardine.png", 8: "Mackerel.png",
                      9: "sadFace.png",0: "Seaweed.png"} 

        #get the url for the image
        image = fishImages.get(fishID)

        #update the fish tally
        if (catch.number < 10):
            self.fish_tally[catch.number] += 1

        #if the fishID doesn't have an image, just default to seaweed for now
        if image == None:
            image = "sadFace.png"

        # TODO add a link to the wikipedia page when you click on the image
        self.ids._fish_image.source = "images/" + image

    def view_fish_tally(self):

        tally_string = "Seaweed: " + str(self.fish_tally[0]) \
                        + "\nTrout: " + str(self.fish_tally[1]) \
                        + "\nSalmon: " + str(self.fish_tally[2]) \
                        + "\nCrayfish: " + str(self.fish_tally[3]) \
                        + "\nShark: " + str(self.fish_tally[4]) \
                        + "\nBoots: " + str(self.fish_tally[5]) \
                        + "\nLobster: " + str(self.fish_tally[6]) \
                        + "\nSardine: " + str(self.fish_tally[7]) \
                        + "\nMackerel: " + str(self.fish_tally[8]) \
                        + "\nFinger: " + str(self.fish_tally[9])

        #TODO create a popup that prints this string
        popup = Popup(size_hint=(None, None), size=(300, 300), title="Total Fish Tally")
        popup.content = Label(text=tally_string)

        popup.open()

class SettingsScreen(Screen):

    #this function will update the user's personal data
    def updateSettings(self):

        user_data = {}
        
        #add the user data to the dictionary if the user entered into the textbox
        if (self.first_name.text != ""):
            user_data["first_name"] = self.first_name.text
        if (self.last_name.text != ""):
            user_data["last_name"] = self.last_name.text

        #try to locate the city/state from the given zipcode
        #if it fails, don't write to the data file
        try:
            int(self.zipcode.text)
            city, state = zip_converter.zip_to_city_state(self.zipcode.text)

            user_data['zip'] = self.zipcode.text
            user_data['city'] = city
            user_data['state'] = state

            #add the user's data to the file
            setup.write_data(user_data)

            self.city_state_label.text = "Location: " + city + ", " + state
        except:
            self.city_state_label.text = "Error: invalid zip code"
    
        #print the user's city/state to the city_state_label
        return

class PizzaScreen(Screen):
    pass

class AddressScreen(Screen):

    def goToOrder(self):

        try:
            #get the customer data and conver to a customer object
            first = self.first_name.text
            last = self.last_name.text
            email = self.user_email.text
            phone = self.user_phone.text
            address = self.user_address.text

            #create customer and pizza objects using the customer info
            customer = Customer(first, last, email, phone, address)
            pizzaOrder = Pizza(customer)

            #send the customer and pizza objects to the main pizza screen
            self.main_pizza_screen.customer = customer
            self.main_pizza_screen.pizzaOrder = pizzaOrder

            #if successful, move to the next screen
            self.manager.current = "Order"
            
        except:
            self.error_label.text = "Error: invalid user input. Try again"
        
class OrderScreen(Screen):
      
    # tracks the contents of your order
    # when something gets added to the list, the order labels will  be updated
    order_list = ListProperty([])
    order_price = NumericProperty(0)

    itemCodes = {"Small Hand Tossed Pizza": "10SCREEN", "Medium Hand Tossed Pizza": "12SCREEN",
                 "Large Hand Tossed Pizza": "14SCREEN", "Medium Pan Pizza": "P12IPAZA",
                 "Boneless wings (14pc)": "W14PBNLW", "Hot Wings (14pc)": "W14PHOTW",
                 "Stuffed Cheesy Bread": "B8PCSCB", " Marbled Cookie Brownie": "MARBRWNE",
                 "Coke(2 Liter)": "2LCOKE", "Diet Coke(2 Liter)": "2LDCOKE", "Sprite(2 Liter)": "2LSPRITE"}
                 
    
    # When the order list property changes, update the order label
    def on_order_list(self, instance, value):
        self.order_label.text = "Your Order: \n\n"
        
        for i in self.order_list:
            self.order_label.text += i + "\n"

    #when the order price property changes, update the price label
    def on_order_price(self, instance, value):
        self.price_label.text = "Total Cost: ${0:.2f}".format(value)
        
    def addToOrder(self, order):
        #if the user chose an item, add it to the list
        if not (order in ["Pizza", "Side", "Drink"]):
            #print the name of the pizza to the order list
            self.order_list.append(order)
            
            #retrieve the itemcodes from the dictionary and add
            #to the pizza object's order
            self.main_pizza_screen.pizzaOrder.addtoOrder(OrderScreen.itemCodes[order])

            #add the item's value to the total price
            self.order_price = 0
            for i in self.main_pizza_screen.pizzaOrder.order.data["Products"]:
                self.order_price += float(i['Price'])

    def clear_order(self):
        
        #reset the pizza object order to an empty list
        self.main_pizza_screen.pizzaOrder.order.data["Products"] = []
        
        #reset the local order_list back to an empty list
        self.order_list = []

        #reset the order price back to 0
        self.order_price = 0

    # goes to the checkout screen if the user is done with their order
    def go_to_checkout(self):

        pizzaOrder = self.main_pizza_screen.pizzaOrder
        
        #change the current screen to the checkout screen
        self.manager.current = "Checkout"

        #update the store and order labels in the checkout screen
        self.checkout_screen.store_label.text = str(pizzaOrder.store)
        self.checkout_screen.order_label.text = "Order:\n"
        for i in self.order_list:
            self.checkout_screen.order_label.text += i + "\n"
        
class CheckoutScreen(Screen):

    #switches betwen carryout and deliver, use the front_order method
    def change_deliv_method(self, deliv_type):
        pizzaOrder = self.main_pizza_screen.pizzaOrder
        if (deliv_type == "Carryout"):
            pizzaOrder.changeToPickup()
        elif (deliv_type == "Delivery"):
            pizzaOrder.changeToDeliv()

    #goes back to the OrderScreen so the user cna change their order
    def change_order(self):
        self.manager.current = "Order"

    #attempt to complete the order, if not, display an error
    def complete_order(self):
        try:
            #retrieve the Pizza object form the main PizzaScreen
            pizzaOrder = self.main_pizza_screen.pizzaOrder

            #attempt to checkout using the Pizza objects's method
            #doesn't actually order the pizza, change the method to placeOrder
            #be warned, it will actually order a pizza if you do that though
            pizzaOrder.testOrder(card = False)

            #if successful, display succes in the Error Label
            self.error_label.text = "Pizza Order Successful! (test only)"

            #TODO add functionality to return to start so they can order again

        except:
            self.error_label.text = "Error: Unsuccessful, perhaps outside of delivery range?"
                        
    
class RecipeScreen(Screen):

    def getRecipe(self):

        try:
            #get the ingredients for the recipe
            ingredients = recipe_finder.main(self.meal_keyword.text)

            #update the panel with teh recipe info
            self.meal_label.text = "Recipe for " + self.meal_keyword.text + ":"
            self.ingredient_box.text = ingredients
            self.meal_keyword.hint_text = ("Enter the meal you want to make here")

        except:
            self.meal_keyword.text= ""
            self.meal_keyword.hint_text = "Error: not specific enough"
        
class DirectionsScreen(Screen):
    def getDirections(self):
        dir_str = directions.locate(self.destination_input.text)
        self.direction_box.text = dir_str

class NewsScreen(Screen):

    def getNews(self):
        source = self.news_input.text
        if ".com" not in source:
            source = source + ".com"
        source = "http://www." + source
        articles = News.getTheNews(source)
        for i in range(5):
            self.top_articles.text += ("Title: " + articles[0][i] + "\n")
            for author in articles[1][i]:
                self.top_articles.text += ("Author: " + author + " ")
            self.top_articles.text += "\n\n"

class LoginPopup(Popup):

    #open the signup screen and close the current login screen
    def openSignupPopup(self):
        SignupPopup().open()
        self.dismiss()

class SignupPopup(Popup):
    pass

class MenuButton(Button):
    pass

class ChatWindow(AnchorLayout):

    #process the user's input from the textinput box
    def processText(self):
        # if the textbox is empty, dont do anything
        if self.text_input.text == '':
            return

        inputString = self.text_input.text
        
        # print the contents of the input to the chat log and reset the input text
        self.text_log.text = self.text_log.text + 'user: ' + inputString + '\n'
        self.text_input.text = ''

        #get the user's response 1 second after they enter the input
        Clock.schedule_once(partial(self.getResponse, inputString), 1)

    def processSpeech(self):

        #get the speech from the user and attempt to convert it to text
        try:
            command = input_converter.myCommand()
            self.text_input.text = command
            self.processText()

        #if speech doesn't work, warn the user
        except AttributeError:
            self.text_input.hint_text = "error: speech not supported atm"
        
    #get the chatbot's response from the backend
    #TODO no backend functionality yet,
    #use output_command here instead of the MemeParserXD class

    def getResponse(self, inputString, dt):

        # TODO only use the command_output file once all commands work
        try:
            self.text_log.text += ("command_output: " + command_output.commands(inputString) + "\n\n")
        except:
            self.text_input.hint_text = "Error: command not recognized"
            self.text_input.text = ""
            
        self.text_input.focus = True

    
class MenuApp(App):
    def build(self):
        return MenuContainer()

if __name__=="__main__":
    MenuApp().run()
