import subprocess
import json
from command_output import say

#function for installing uninstalled modules
def install(name):
    subprocess.call("python -m pip install --upgrade " + name, shell=True)

def update_modules():
    #update pip if necessary
    subprocess.call("python -m pip install --upgrade pip", shell=True)

    #install various necessary modules
    try:
        import darksky
    except ImportError:
        print("ERROR!!!!")
        install('darkskylib')
    try:
        import uszipcode
    except ImportError:
        install('uszipcode')
    try:
        import kivy
    except ImportError:
        install('kivy')
    try:
        import pyaudio
    except ImportError:
        install('pyaudio')
    try:
        import speech_recognition
    except ImportError:
        install('speech_recognition')
    try:
        import gtts
    except ImportError:
        install('gtts')
    try:
        import pyttsx3
    except ImportError:
        install('pyttsx3')
    try:
        import keyboard
    except ImportError:
        install('keyboard')
    try:
        import pizzapi
    except ImportError:
        install(pizzapi)
    try:
        import nltk
    except ImportError:
        install('nltk')
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')

#create the initial user data
def initial_data():
    user_data = {}
    user_data["first_name"] = input("First Name: ").lower()
    user_data["last_name"] = input("Last Name: ").lower()
    user_data["age"] = input("Age: ").lower()
    user_data["zip"] = input("Zip Code: ").lower()
    user_data["city"] = input("City: ").lower()
    user_data["state"] = input("State (Ex: ri, nh, ca): ").lower()
    return user_data

#write user data to a json file
def write_data(user_data):
    data = open("userData.json", "w+")
    #write the data to the file
    with data as outfile:
        json.dump(user_data, outfile)

#get the information from the data file for various uses
def get_data():
    with open("userData.json") as json_file:
        data = json.load(json_file)
        return data

#Access settings to be able to view and alter user data
def settings():
    #specify user data that needs to go into this file
    user_data = get_data()
    for key in user_data:
        print (key, 'corresponds to', user_data[key])
    say(user_data)
    write_data(user_data)
    return user_data

def main():
    update_modules()
    user_data = initial_data()
    write_data(user_data)