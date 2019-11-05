#Python 2.x program to transcribe an Audio file 
import speech_recognition as sr 

AUDIO_FILE = ("Test1.wav") 

# use the audio file as the audio source 

r = sr.Recognizer() 

with sr.AudioFile(AUDIO_FILE) as source: 
	#reads the audio file. Here we use record instead of 
	#listen 
	audio = r.record(source) 

print("The audio file contains: " + r.recognize_google(audio)) 


# Import the required module for text 
# to speech conversion 
from gtts import gTTS 

# This module is imported so that we can 
# play the converted audio 
import os 

# The text that you want to convert to audio 
mytext =  r.recognize_google(audio)

#"Twinkle twinkle little star how I wonder what you are up above the world so high like a diamond in the sky twinkle twinkle little star how I wonder what you are when the blazing sun is born when he nothing shines upon then you show your little light twinkle twinkle all the night twinkle twinkle little star how I wonder what you are"

# Language in which you want to convert 
language = 'en'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed 
myobj = gTTS(text=mytext, lang=language, slow=False) 

# Saving the converted audio in a mp3 file named 
# welcome 
myobj.save("output.mp3") 

# Playing the converted file 
os.system("xdg-open output.mp3") 

