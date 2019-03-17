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

class CalendarScreen(Screen):
    pass

class WeatherScreen(Screen):
    pass

class MemeScreen(Screen):
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
