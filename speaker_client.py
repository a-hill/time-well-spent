import time
import requests
import sys
from espeak import espeak
import os

poll_rate = 0.4  # in seconds
url = 'http://modern-times-1.uksouth.cloudapp.azure.com:5555'
door = int(sys.argv[1])

def play_sound(total_time_pp):
    hours = int(total_time_pp / 3600)
    minutes = int((total_time_pp % 3600) / 60)
    seconds = int(total_time_pp % 60)

    hours_speech = str(hours) + " hours " if hours != 0 else ''
    mins_speech = str(minutes) + " minutes " if minutes != 0 else ''
    seconds_speech = str(seconds) + " seconds "

    speech = hours_speech + mins_speech + seconds_speech
    os.system("espeak '" + speech + "'")

for i in range(10):
    play_sound(i * 10)

#while True:
#    r = requests.get(url + '/next_exit_time/' + str(door) + '/')

#    try:
#        seconds = int(r.text)
#        play_sound(seconds)
#    except ValueError:
#        print("no sound to play")

#    print 'speaker client request text: ' + r.text
#    time.sleep(poll_rate)
