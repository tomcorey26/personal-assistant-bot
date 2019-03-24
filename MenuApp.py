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

from sampleParser import memeParserXD as mp
import time
from fish import Fish
import random

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
    pass

class WeatherScreen(Screen):
    pass

class TwitterScreen(Screen):
    pass

class RedditScreen(Screen):
    pass

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
