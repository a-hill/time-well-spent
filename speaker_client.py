import time
import requests
import sys
from multiprocessing import Process
import os
import json
from Queue import PriorityQueue
from termcolor import colored
from gtts import gTTS

poll_rate = 0.1  # in seconds
url = 'http://modern-times-1.uksouth.cloudapp.azure.com:5000'
door = int(sys.argv[1])
speed = "175"  # Speed in wpm. Default is 175, min is 80, theoretical max is 500
pitch = "50"  # Pitch between 0 and 99, default is 50
variant = "m1"  # can be m1-6 or f1-6 or whisper or croak

def say_phrase(string):
    tts = gTTS(text=string, lang='en')
    filename = 'temp.mp3'
    tts.save(filename)
    time.sleep(0.1)
    
    try:    
        os.system('cvlc ' + filename + ' --play-and-exit >/dev/null 2>/dev/null')
        os.remove(filename)
    except:
        print colored('WARNING OS ERROR IN SPEAKER', 'red')

def play_sound(total_time_pp):
    hours = int(total_time_pp / 3600)
    minutes = int((total_time_pp % 3600) / 60)
    seconds = int(total_time_pp % 60)

    hours_speech = str(hours) + " hours " if hours != 0 else ''
    mins_speech = str(minutes) + " minutes " if minutes != 0 else ''
    seconds_speech = str(seconds) + " seconds "

    speech = hours_speech + mins_speech + seconds_speech
    print colored('about to say: \'' + speech + '\'', 'green')

    say_phrase(speech)

def should_say(last_message,  this_message):
    return abs(last_message - this_message)
	

last_message_said = 0

print_freq = 20
count = 0
while True:

    r = ''
    try:
        r = requests.get(url + '/next_exit_time/' + str(door) + '/')
    except requests.exceptions.ConnectionError:
        print colored('speaker on door: ' + str(door) + ' failed to connect to server', 'red')
    else:
        if r.text != 'no sound to play':
            time_spent = int(r.text)
            if should_say(last_message_said, time_spent):
                play_sound(time_spent)
                last_message_said = time_spent
            else:
                print colored('Not saying time', 'yellow')
        else:
            if count % print_freq == 0:
                print count, ': no sound to play'
            count += 1
                
    time.sleep(poll_rate)
