import os, atexit
import input_converter, command_output, setup

def main():
    # remove the guest file when the program closes
    atexit.register(setup.del_guest)
    #get input from the user
    input_list = ["settings", "tell me a joke.", "weather in south kingstown ri", "what's the weather in narragansett ri", "tell me the weather in new york ny", "the weather"]
    #command_input = input_list[1]
    #command_input = input("Command: ")
    command_input = input_converter.myCommand()
    command = input_converter.convert_text(command_input.lower())
    #use input for command output
    command_output.commands(command)

#find out if user is logging in as a guest
while True:
    #ask for a yes or no answer
    guest_answer = input("Are you a guest?(y/n) ")
    #if yes, go through guest settings
    if guest_answer.lower() == 'y':
        setup.is_guest = True
        break
    #if no, continue as a normal user
    elif guest_answer.lower() == 'n':
        setup.is_guest = False
        break
    #if neither of these inputs, try again
    else: continue


#run setup if the userData file hasn't been created yet or the user is a guest
if (not os.path.exists("user_data.json")) or (setup.is_guest == True):
    print("Creating file now...")
    setup.main()
#once it does exist, start running the program
main()