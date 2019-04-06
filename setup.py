import subprocess
import json

#create guest variable
is_guest = False

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
        install('darkskylib')
    try:
        import uszipcode
    except ImportError:
        install('uszipcode')
    try:
        import kivy
    except ImportError:
        install('docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew')
        install('kivy.deps.angle')
        install('kivy')
    try:
        import pyaudio
    except ImportError:
        install('pyaudio')
    try:
        import speech_recognition
    except ImportError:
        install('SpeechRecognition')
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
        import googlesearch
    except ImportError:
        install("beautifulsoup4")
        install("google")
    try:
        import pizzapi
    except ImportError:
        install('pizzapi')

    try:
        import pizzapy
    except ImportError:
        install('git+https://github.com/Magicjarvis/pizzapi.git')
    try:
        import newspaper
    except ImportError:
        install('newspaper3k')
    try:
        import praw
    except ImportError:
        install('praw')
    try:
        import recipe_scrapers
    except ImportError:
        install("git+git://github.com/hhursev/recipe-scrapers.git")
    try:
        import geocoder
    except ImportError:
        install('geocoder')
    try:
        import nltk
        install('nltk')
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        nltk.download('brown')
        nltk.download('maxent_treebank_pos_tagger')
        nltk.download('wordnet')
    except ImportError:
        install('nltk')
        import nltk
        install('nltk')
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        nltk.download('brown')
        nltk.download('maxent_treebank_pos_tagger')
        nltk.download('wordnet')

#create the initial user data
def initial_data():
    from zip_converter import zip_to_city_state
    user_data = {}
    user_data["first_name"] = input("First Name: ").lower()
    user_data["last_name"] = input("Last Name: ").lower()
    user_data["zip"] = input("Zip Code: ").lower()
    user_data["city"], user_data["state"] = zip_to_city_state(user_data["zip"])
    print(user_data)

    return user_data

#write user data to a json file
def write_data(user_data):
    #if user is guest, create a guest file
    if is_guest:
        data = open("guest_data.json", "w+")
    #otherwise, write the data to the file
    else:
        # open the specific user file
        data = open("user_data.json", "w+")
    #write data to the file
    with data as outfile:
        json.dump(user_data, outfile)
    data.close()

#get the information from the data file for various uses
def get_data():
    #if guest user, get the data from the guest file
    if is_guest:
        file_name = "guest_data.json"
    #if not guest, get the data from the user file
    else:
        file_name = "user_data.json"
    #get the data from whatever file is being accessed
    with open(file_name) as json_file:
        data = json.load(json_file)
        return data

#Access settings to be able to view and alter user data
def settings():
    #specify user data that needs to go into this file
    user_data = get_data()
    try:
        for key in user_data:
            print (key, 'corresponds to', user_data[key])
        write_data(user_data)
    except IndexError:
        user_data = {}
    return user_data

def del_guest():
    from pathlib import Path
    import os
    #define the file that needs to be removed
    guest_file = Path("guest_data.json")
    #remove it if it exists
    if guest_file.exists():
        print("File found! " + str(guest_file))
        os.remove(str(guest_file))

def main():
    update_modules()
    user_data = initial_data()
    write_data(user_data)
