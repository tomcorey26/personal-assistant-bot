import subprocess
import json
from sys import version_info

#create guest variable
is_guest = False

#function for installing uninstalled modules
def install(name):
    subprocess.call("python -m pip install --upgrade " + name, shell=True)

def update_modules():
    #update pip if necessary
    install("pip")

    #install various necessary modules
    try:
        import darksky
    except ImportError:
        print("darksky not found")
        install('darkskylib')
        
    try:
        import uszipcode
    except ImportError:
        print("uszipcode not found")
        install('uszipcode')
        
    try:
        from kivy.uix.label import Label
    except ImportError:
        print("error, kivy not found")
        install('docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew')
        install('kivy.deps.angle')
        install('kivy')
        print("done installing kivy")
        
    try:
        import pyaudio
    except ImportError:
        print("pyaudio not found")
        
        #need to install from a custom wheel if python version 3.7
        if (version_info[0] == 3 and version_info[1] == 7):
            install('PyAudio-0.2.11-cp37-cp37m-win32.whl')
        else:
            install('pyaudio')
            
    try:
        import speech_recognition
    except ImportError:
        print("speech_recognition not found")
        install('SpeechRecognition')
        
    try:
        import gtts
    except ImportError:
        print("gtts not found")
        install('gtts')
        
    try:
        import pyttsx3
    except ImportError:
        print("pyttsx3 not found")
        install('pyttsx3')
        
    try:
        import keyboard
    except ImportError:
        print("keyboard not found")
        install('keyboard')
        
    try:
        import googlesearch
    except ImportError:
        print("googlesearch not found")
        install("beautifulsoup4")
        install("google")
        
    try:
        import pizzapi
    except ImportError:
        print("pizzapi not found")
        install('pizzapi')

    try:
        import pizzapy
    except ImportError:
        print("pizzapy not found")
        install('git+https://github.com/Magicjarvis/pizzapi.git')
        
    try:
        import newspaper
    except ImportError:
        print("newspaper not found")
        install('newspaper3k')
        
    try:
        import praw
    except ImportError:
        print("praw not found")
        install('praw')
        
    try:
        import recipe_scrapers
    except ImportError:
        print("recipe_scrapers not found")
        install("git+git://github.com/hhursev/recipe-scrapers.git")
        
    try:
        import geocoder
    except ImportError:
        print("geocoder not found")
        install('geocoder')
        
    try:
        import openrouteservice
    except ImportError:
        print("openrouteservice not found")
        install("openrouteservice")
        
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
        print("nltk not found")
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

    try:
        import tweepy
    except:
        print("tweepy not found")
        install('tweepy')

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

if __name__ == "__main__":
    main()
