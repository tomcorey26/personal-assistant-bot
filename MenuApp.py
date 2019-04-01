#disable multitouch functionality
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

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
from kivy.properties import ListProperty

from sampleParser import memeParserXD as mp
import time
from fish import Fish
import random
import calendar_events as events
import RedditApi
import weather
import location_to_coords


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
            self.event_label.text = "events for " + dateString + ":\n" \
                                    + "    TODO: add event here"
        
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
    pass

class RedditScreen(Screen):

    def getPosts(self):
        posts = RedditApi.redditPosts(5, self.subreddit_input.text)

        self.top_posts.text = ""
        
        for (name, url) in posts.items():
            self.top_posts.text += (name + "\n" + url + "\n\n")
        

class FishScreen(Screen):

    def castLine(self):
        fishID = random.randint(0, 20)
        catch = Fish(fishID)
        species, wikiURL = catch.getSpecies()

        if (species != "You fail to catch a fish"):
            species = "You caught a " + species
        self.ids._catch_label.text = species

        #dictionary of the image URL's
        #TODO find a better way to implement these

        imageURLs = {1: "Trout.png", 2: "Salmon.png", 5: "Boots.png", 7: "Cod.png", 0: "Seaweed.png"} 

        #get the url for the image
        url = imageURLs.get(fishID)

        #if the fishID doesn't have an image, just default to seaweed for now
        if url == None:
            url = "Seaweed.png"

        self.ids._fish_image.source = "images/" + url

    
class SettingsScreen(Screen):
    pass

class PizzaScreen(Screen):
    pass

class OrderScreen(Screen):

    # tracks the contents of your order
    # when something gets added to the list, the order label will  be updated
    order_list = ListProperty([])

    # when the "add to order" button is pressed, adds the pizza to the order list
    def addPizza(self):
        self.order_list.append(self.size_btn.text + " " + self.toppings_btn.text + " Pizza")

    def addSides(self):
        side = self.side_btn.text
        drink = self.drink_btn.text

        #add the side/drink if the user has selected one
        if (side != "Side" and side != "None"):
            self.order_list.append(side)

        if (drink != "Drink" and drink != "None"):
            self.order_list.append(drink)

        #reset the side/drink buttons to the default
        self.side_btn.text = "Side"
        self.drink_btn.text = "Drink"

    # When the order list property changes, update the order label to reflect the list
    def on_order_list(self, instance, value):
        self.order_label.text = "Your Order: \n\n"

        for i in self.order_list:
            self.order_label.text += i + "\n"

    # goes to the checkout screen if the user is done with their order
    def go_to_checkout(self):

        #send the order list to the checkout screen
        checkout_screen = self.manager.checkout_screen
        checkout_screen.order_list = self.order_list

        #change the current screen to the checkout screen
        self.manager.current = "Checkout"
        
class CheckoutScreen(Screen):
    order_list = ListProperty([])

    def on_order_list(self, instance, value):
        self.ids._main_label.text = str(self.order_list)
    
class RecipeScreen(Screen):
    pass

class NewsScreen(Screen):
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


    #get the chatbot's response from the backend
    #TODO no backend functionality yet
    def getResponse(self, inputString, dt):
        self.text_log.text = self.text_log.text + "bot: " + mp.parse(self, inputString) + '\n\n'
        self.text_input.focus = True

    
class MenuApp(App):
    def build(self):
        return MenuContainer()

if __name__=="__main__":
    MenuApp().run()
