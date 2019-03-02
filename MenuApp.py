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

from sampleParser import memeParserXD as mp
import time

Builder.load_file('menubar.kv')
Builder.load_file('chatwindow.kv')
Builder.load_file('screens.kv')

class MenuContainer(AnchorLayout):
    pass

class MenuManager(ScreenManager):
    pass

class CalendarScreen(Screen):
    pass

class WeatherScreen(Screen):
    pass

class MemeScreen(Screen):
    pass

class MenuButton(Button):
    def switchScreens(self):
        self.parent.screen_manager.current = self.text

class ChatWindow(AnchorLayout):
    
    def processText(self):
        # if the textbox is empty, dont do anything
        if self.text_input.text == '':
            return

        inputString = self.text_input.text
        
        # print the contents of the input to the chat log and reset the input text
        self.text_log.text = self.text_log.text + 'user: ' + inputString + '\n'
        self.text_input.text = ''

        # TODO figure a way to add delay to the function using kivy.clock, doesn't work as currently configured
        # Clock.schedule_once(lambda dt: self.doNothing(), 1)
        
        # print the bot's response
        self.text_log.text = self.text_log.text + "bot: " + mp.parse(inputString) + '\n'

    def doNothing(dt):
        pass
    
class MenuApp(App):
    def build(self):
        return MenuContainer()

if __name__=="__main__":
    MenuApp().run()
