import os

import sys 
import time
import time
import RPi.GPIO as GPIO       ## Import GPIO library

GPIO.setmode(GPIO.BOARD)      ## Use board pin numbering
GPIO.setup(3, GPIO.OUT)      ## Setup GPIO Pin 11 to OUT
GPIO.setup(5, GPIO.OUT)      ## Setup GPIO Pin 11 to OUT
GPIO.setup(7, GPIO.OUT)      ## Setup GPIO Pin 11 to OUT
GPIO.setup(11, GPIO.OUT)      ## Setup GPIO Pin 11 to OUT


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
    
watch_file = os.environ['HOME'] + '/Downloads/control.txt'

open(watch_file, 'a').close()

light = fan = ac  = tv = 0

# watcher = Watcher(watch_file)  # simple
watcher = Watcher(watch_file, custom_action, text='')  # also call custom action function
watcher.watch()  # start the watch going

os.remove(watch_file)

print("Ready")

while True:
    flag = False
    while not watcher.watch():
        pass
    
    filepath = watch_file
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            if int(line[0]) == 0:
                if int(line[2]) == 0:
                    fan = 0
                else:
                    fan = 1
                    
            if int(line[0]) == 1:
                if int(line[2]) == 0:
                    light = 0
                else:
                    light = 1
                    
            if int(line[0]) == 2:
                if int(line[2]) == 0:
                    ac = 0
                else:
                    ac = 1
                    
            if int(line[0]) == 3:
                if int(line[2]) == 0:
                    tv = 0
                else:
                    tv = 1
            
            GPIO.output(3, light)
            GPIO.output(5, fan)
            GPIO.output(7, ac)
            GPIO.output(11, tv)
    
    print(light)
    print(fan)
    print(ac)
    print(tv)
    
    os.remove(watch_file)

