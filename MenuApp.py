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

#import all of the local python files that the group created
from sampleParser import memeParserXD as mp
import time
from fish import Fish
import random
import calendar_events as events
import RedditApi
import weather
import location_to_coords
from front_order import *
import input_converter
import recipe_finder
import zip_converter
import setup
import TwitterApi


Builder.load_file('menubar.kv')
Builder.load_file('chatwindow.kv')
Builder.load_file('screens.kv')

class MenuContainer(AnchorLayout):

    #constructor
    def __init__(self, **kwargs):
        super(MenuContainer, self).__init__(**kwargs)

        #load the login popup when the app starts
        Clock.schedule_once(LoginPopup().open, 0)

class MenuManager(ScreenManager):

    #change the current screen to the one with the specified name
    def switchScreens(self, name):
        self.current = name

# TODO maybe it would be better to make a screens.py file
# where all of teh screens functions can be stored.
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
        
        #save the string from the textbox and set the textbox to empty
        location = self.location_input.text
        self.location_input.text = ""

        #convert the location into latitude and longitude
        lat, lon, cityname = location_to_coords.main(location)

        #if the city isn't found, let the user know of the error
        if cityname == 'Unrecognized location':
            self.location_input.hint_text = "Error, location not found"
            self.location_input.hint_color = (1, .3, .3, 1)

        #otherwise, print out the current weather for that city
        else:
            
            #reset the userinput hint, in case they had an error before
            self.location_input.hint_text = "Enter zipcode, city, or city/state"
            self.location_input.hint_color = (.2, .2, .2, 1)
            
            #display the name of the city
            self.city_label.text = "Weather for " + cityname + ":"
            
            #display the city's weather
            temp, summ, icon, humid = weather.getCurrentWeather(lat, lon)
            self.temp_button.text = "Temperature:\n" + str(temp)
            self.summary_button.text = "Summary:\n" + str(summ)
            self.image_button.text = "imageurl:\n" + str(icon) + ".png"
            self.humidity_button.text = "Humidity:\n" + str(humid * 100) + "%"

class TwitterScreen(Screen):

    def getTweets(self):
        user = self.twitter_input.text

        self.recent_tweets.text = ""

        twitter = TwitterApi.TwitterScrape(5, user)
        posts = twitter.grabRecentPosts()
        for status in posts:
            self.recent_tweets.text += status.text + '\n'

class RedditScreen(Screen):

    def getPosts(self):
        posts = RedditApi.redditPosts(5, self.subreddit_input.text)

        self.top_posts.text = ""
        
        for (name, url) in posts.items():
            self.top_posts.text += (name + "\n" + url + "\n\n")
        

class FishScreen(Screen):

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
        fishImages = {1: "Trout.png", 2: "Salmon.png", 3:"Crayfish.png", 4:"Minnow.png",
                      5: "Boots.png", 6: "Lobster.png", 7: "Sardine.png", 8: "Mackerel.png",
                      9: "sadFace.png",0: "Seaweed.png"} 

        #get the url for the image
        image = fishImages.get(fishID)

        #if the fishID doesn't have an image, just default to seaweed for now
        if image == None:
            image = "sadFace.png"

        self.ids._fish_image.source = "images/" + image

    
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

    # goes to the checkout screen if the user is done with their order
    def go_to_checkout(self):

        #change the current screen to the checkout screen
        self.manager.current = "Checkout"

        #send the checkokut screen any info it needs
        
class CheckoutScreen(Screen):
    pass
    
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
    pass


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
        self.text_log.text += ("bot: " + mp.parse(self, inputString) + '\n\n')
        self.text_input.focus = True

    
class MenuApp(App):
    def build(self):
        return MenuContainer()

if __name__=="__main__":
    MenuApp().run()
