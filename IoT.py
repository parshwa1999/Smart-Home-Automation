#Python 2.x program to transcribe an Audio file 
import speech_recognition as sr 

# Import the required module for text 
# to speech conversion 
from gtts import gTTS 
from nltk.tokenize import word_tokenize

# This module is imported so that we can 
# play the converted audio 

import paramiko
from scp import SCPClient

import os

import sys 
import time

# Language in which you want to convert 
language = 'en'

AUDIO_FILE = (os.environ['HOME'] + "/Downloads/download.wav") 

open(AUDIO_FILE, 'a').close()

fan = light = tv = ac = False

# use the audio file as the audio source 

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

ssh = createSSHClient('10.20.24.19', '22', 'pi', 'raspberry')
scp = SCPClient(ssh.get_transport())

r = sr.Recognizer()

class Watcher(object):
    running = True
    refresh_delay_secs = 1

    # Constructor
    def __init__(self, watch_file, call_func_on_change=None, *args, **kwargs):
        self._cached_stamp = 0
        self.filename = watch_file
        self.call_func_on_change = call_func_on_change
        self.args = args
        self.kwargs = kwargs

    # Look for changes
    def look(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
            # print('File changed')
            if self.call_func_on_change is not None:
                self.call_func_on_change(*self.args, **self.kwargs)
            return 1
        return 0

    # Keep watching in a loop        
    def watch(self):
        while self.running: 
            try: 
                # Look for changes
                time.sleep(self.refresh_delay_secs) 
                return self.look()
            except KeyboardInterrupt: 
                print('\nDone') 
                break 
            except FileNotFoundError:
                # Action on file not found
                pass
            except: 
                print('Unhandled error: %s' % sys.exc_info()[0])

# Call this function each time a change happens
def custom_action(text):
    print(text)

watch_file = AUDIO_FILE

# watcher = Watcher(watch_file)  # simple
watcher = Watcher(watch_file, custom_action, text='')  # also call custom action function
watcher.watch()  # start the watch going

os.remove(AUDIO_FILE)

print("Ready! ")

while True:
    flag = False
    while not watcher.watch():
        pass
    
    print("change detected")

    try:
        with sr.AudioFile(AUDIO_FILE) as source: 
	        #reads the audio file. Here we use record instead of 
	        #listen 
	        audio = r.record(source) 

        mytext = r.recognize_google(audio)

        print("The audio file contains: " + mytext) 
    
    except:
        myobj = gTTS(text='Did not quite catch that, please repeat', lang=language, slow=False)
        myobj.save("output.mp3")
        #os.system("xdg-open output.mp3")
        os.remove(AUDIO_FILE)
        continue
    # Fan
    
    tokenized = word_tokenize(mytext)
    
    f = open('control.txt', 'w')
    
    if ('fan' in tokenized or 'fans' in tokenized) and 'on' in tokenized:
        flag=True
        if fan == False:
            myobj = gTTS(text='Turning on fan', lang=language, slow=False)
            fan = True
            f.write('0 1\n')
        else:
            myobj = gTTS(text='Fans already turned on', lang=language, slow=False)
        
        myobj.save("output.mp3")
        #os.system("xdg-open output.mp3")
        
    elif ('fan' in tokenized or 'fans' in tokenized) and 'off' in tokenized:
        flag=True
        
        if fan == True:
            myobj = gTTS(text='Turning off fan', lang=language, slow=False)
            fan = False
            f.write('0 0\n')
        else:
            myobj = gTTS(text='Fans already turned off', lang=language, slow=False)
        myobj.save("output.mp3")
        #os.system("xdg-open output.mp3")

    # Light

    if ('light' in tokenized or 'lights' in tokenized) and 'on' in tokenized:
        flag=True
        
        if light == False:
            myobj = gTTS(text='Turning on lights', lang=language, slow=False)
            light = True
            f.write('1 1\n')
        else:
            myobj = gTTS(text='Lights already turned on', lang=language, slow=False)
        
        myobj.save("output.mp3")
        #os.system("xdg-open output.mp3")
    elif ('light' in tokenized or 'lights' in tokenized) and 'off' in tokenized:
        flag=True
        if light == True:
            myobj = gTTS(text='Turning off lights', lang=language, slow=False)
            light = False
            f.write('1 0\n')
        else:
            myobj = gTTS(text='Lights already turned off', lang=language, slow=False)
        myobj.save("output.mp3")
        #os.system("xdg-open output.mp3")

    # Air Conditioner

    if ('air' in tokenized and ('conditioner' in tokenized or 'conditioners' in tokenized) and 'on' in tokenized):
        flag=True
        
        if ac == False:
            myobj = gTTS(text='Turning on air conditioner', lang=language, slow=False)
            ac = True
            f.write('2 1\n')
        else:
            myobj = gTTS(text='Air conditioner already turned on', lang=language, slow=False)
        
        myobj.save("output.mp3")
        #os.system("xdg-open output.mp3")
    elif ('air' in tokenized and ('conditioner' in tokenized or 'conditioners' in tokenized) and 'off' in tokenized):
        flag=True
        
        if ac == True:
            myobj = gTTS(text='Turning off air conditioner', lang=language, slow=False)
            ac = False
            f.write('2 0\n')
        else:
            myobj = gTTS(text='Air conditioner already turned off', lang=language, slow=False)
        myobj.save("output.mp3")
        #os.system("xdg-open output.mp3")

    # Television

    if ('television' in tokenized or 'televisions' in tokenized) and 'on' in tokenized:
        flag=True
        if tv == False:
            myobj = gTTS(text='Turning on television', lang=language, slow=False)
            tv = True
            f.write('3 1\n')
        else:
            myobj = gTTS(text='Television already turned on', lang=language, slow=False)
        myobj.save("output.mp3")
        #os.system("xdg-open output.mp3")
    elif ('television' in tokenized or 'televisions' in tokenized) and 'off' in tokenized:
        flag=True
        
        if tv == True:
            myobj = gTTS(text='Turning off television', lang=language, slow=False)
            tv = False
            f.write('3 0\n')
        else:
            myobj = gTTS(text='Television already turned off', lang=language, slow=False)
        myobj.save("output.mp3")
        #os.system("xdg-open output.mp3")
    
    if not flag:
        myobj = gTTS(text='Did not quite catch that, please repeat', lang=language, slow=False)
        myobj.save("output.mp3")
        #os.system("xdg-open output.mp3")
    
    f.close()
    
    os.remove(AUDIO_FILE)
    
    scp.put('output.mp3', '/home/pi/Downloads/output.mp3')
    scp.put('control.txt', '/home/pi/Downloads/control.txt')
