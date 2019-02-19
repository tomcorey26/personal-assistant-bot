import os
import nltk
import keyboard
from gtts import gTTS
import speech_recognition as sr

#CALL THIS WHENEVER YOU WANT TO SPEAK SOMETHING TO THE SYSTEM
def myCommand():
    #listens for commands
    r = sr.Recognizer()

    #listens to microphone audio
    with sr.Microphone() as source:
        print("Ready...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    #attemptd to process that audio into text
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand()

    return command

def phrase_conversion(tagged_chunks):
    for subtree in tagged_chunks.subtrees():
        #find all chunks labeled as noun phrases and join their pieces into single strings
        if subtree.label() == 'CM':
          yield ' '.join(word for word, tag in subtree.leaves())

def convert_text(input):
    #separate the sentence into words and punctuation
    tokens = nltk.word_tokenize(input)
    print(tokens)

    #remove useless words (and, is, the, a, etc.)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    clean_tokens = [w for w in tokens if not w in stop_words]
    print("clean: ", clean_tokens)

    #tag remaining words with parts of speech
    tagged = nltk.pos_tag(tokens)
    print("Tagged: ", tagged)

    #chunk common phrases using a chunk grammar
    grammar = "CM: {<VB>|<JJ.*>*<NN.*>+}"
    cp = nltk.RegexpParser(grammar)
    #using the pattern in the grammer, chunks are put into noun phrases
    result = cp.parse(tagged)
    print("Chunked: ", result)

    #combine separated noun phrases into full strings
    phrases = []
    for full_string in phrase_conversion(result):
        #append these combined noun phrases to a string
        phrases.append(full_string)
    print("Phrases: ", phrases)

    #pass the array of phrases to the command function
    return phrases
