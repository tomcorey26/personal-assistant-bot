import subprocess
import struct
import json
from sys import version_info

#create guest variable
is_guest = False

#function for installing uninstalled modules
def install(name):
    subprocess.call("python -m pip install --upgrade " + name, shell=True)

def update_modules():
    #update pip if necessary
    print("updating pip")
    install("pip")

    #install various necessary modules
    print("installing Darksky")
    install('darkskylib')

    print("installing uszipcode")
    install('uszipcode')

    print("installing kivy")
    install('docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew')
    install('kivy.deps.angle')
    install('kivy')

    print("installing pyaudio")
    #need to install from a custom wheel if python version 3.7
    #check for 32 bit or 64 bit
    py_vers = struct.calcsize("P") * 8
    if (version_info[0] == 3) and (version_info[1] == 7):
        if py_vers == 32:
            print("32 bit version detected")
            install('PyAudio-0.2.11-cp37-cp37m-win32.whl')
        elif py_vers == 64:
            print('64 bit version detected')
            install('PyAudio-0.2.11-cp37-cp37m-win_amd64.whl')
    else:
        install('pyaudio')

    print("installing speech_recognition")
    install('SpeechRecognition')

    print("installing gtts")
    install('gtts')

    print("installing pyttsx3")
    install('pyttsx3')

    print("installing keyboard")
    install('keyboard')

    print("installing googlesearch")
    install("beautifulsoup4")
    install("google")

    print("installing pizzapi")
    install('pizzapi')

    print("installing pizzapy")
    install('git+https://github.com/Magicjarvis/pizzapi.git')

    print("installing praw")
    install('praw')

    print("installing recipe_scrapers")
    install("git+git://github.com/hhursev/recipe-scrapers.git")

    print("installing geocoder")
    install('geocoder')

    print("installing openrouteservice")
    install("openrouteservice")

    print("installing nltk")
    install('nltk')

    print("installing tweepy")
    install('tweepy')

    print("installing newspaper3k")
    install('newspaper3k')

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
