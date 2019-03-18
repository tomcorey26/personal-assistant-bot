import time
class memeParserXD:

    def parse(chatWindow, textInput):

        output = ''
        if textInput == "fish":
            chatWindow.screen_manager.current = "Fishing"
            output = "sup, my dudes"
        elif textInput == "weather":
            output = "it\'s pretty good outside"
            chatWindow.screen_manager.current = "Weather"
        elif textInput == "calendar":
            output = "yea theres a calendar"
            chatWindow.screen_manager.current = "Calendar"
        else:
            output = "idk what that means"

        return output
        
