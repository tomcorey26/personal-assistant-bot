import input_converter
import command_output

#get input from the user
input = input_converter.myCommand()
#input = input("Command: ")
command = input_converter.convert_text(input.lower())

#use input for command output
command_output.commands(command)
