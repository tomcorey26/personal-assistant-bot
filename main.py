import input_converter
import os
import command_output
import setup

def main():
    #get input from the user
    input_list = ["weather in south kingstown ri", "what's the weather in narragansett ri", "tell me the weather in new york ny", "the weather"]
    #command_input = input_list[0]
    command_input = input("Command: ")
    #command_input = input_converter.myCommand()
    command = input_converter.convert_text(command_input.lower())
    #use input for command output
    command_output.commands(command)

#run setup if the userData file hasn't been created yet
if not os.path.exists("userData.json"):
    print("Creating file now...")
    setup.main()
#once it does exist, start running the program
main()