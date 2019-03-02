import time
class memeParserXD:

    def parse(textInput):

        output = ''
        if textInput == "fun":
            output = "sup, my dudes"
        elif textInput == "weather":
            output = "it\'s pretty good outside"
        elif textInput == "calendar":
            output = "yea theres a calendar"
        else:
            output = "idk what that means"

        time.sleep(1)
        return output
        
