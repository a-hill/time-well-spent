import time
import requests
import sys
import pyttsx
import inflect

poll_rate = 0.5 #in seconds
url = 'http://modern-times-1.uksouth.cloudapp.azure.com:5000'
door = int(sys.argv[1])

def play_sound(total_time_pp):
    hours = int(total_time_pp / 3600)
    minutes = int((total_time_pp % 3600) / 60)
    seconds = int(total_time_pp % 60)
    
    speak = inflect.engine()
    hours_speech = ""
    mins_speech = ""
    seconds_speech = "" 
    if hours is not 0:
        hours_speech = speak.number_to_words(hours) + "hours"
    if minutes is not 0:
        mins_speech = speak.number_to_words(minutes) + "minutes"
    if seconds is not 0:
        seconds_speech = speak.number_to_words(seconds) + "seconds"
        
    speech = hours_speech + mins_speech + seconds_speech
    sound = pyttsx.init()
    sound.say(speech)
    sound.runAndWait()

while True:
    r = requests.get(url + '/next_exit_time/' + str(door) + '/'
    if r.text != 'no sound to play':
   		play_sound(r.text)
   
    print 'speaker client request text: ' + r.text
    time.sleep(poll_rate)
