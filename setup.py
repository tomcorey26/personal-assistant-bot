import subprocess

#function for installing uninstallled modules
def install(name):
    subprocess.call("python -m pip install --upgrade " + name, shell=True)

#update pip if necessary
print(subprocess.call("python -m pip install --upgrade pip", shell=True))
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
    import nltk
except ImportError:
    install('nltk')
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')