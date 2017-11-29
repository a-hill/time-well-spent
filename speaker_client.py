import time
import requests
import sys
from multiprocessing import Process
import os
import json
from Queue import PriorityQueue
from termcolor import colored

MAX_TIME_PASSED = 1 # in seconds
poll_rate = 0.4  # in seconds
url = 'http://modern-times-1.uksouth.cloudapp.azure.com:5000'
door = int(sys.argv[1])
speed = "175"  # Speed in wpm. Default is 175, min is 80, theoretical max is 500
pitch = "50"  # Pitch between 0 and 99, default is 50
variant = "m1"  # can be m1-6 or f1-6 or whisper or croak
#priorityQueue = PriorityQueue()


#def __init__():
#    process = Process(target=run)
#    process.start()


#def run():
#    while True:
#        print 'polling the server...'
#        
#        r = ''
#        try:
#            r = requests.get(url + '/next_exit_time/' + str(door) + '/')
#        except requests.exceptions.ConnectionError:
#            print colored('speaker on door: ' + str(self.door) + ' failed to connect to server', 'yellow')
#        else:
#            body = json.loads(r.text)

#            if not body['sound'] is 'false':
#                try:
#                    seconds = int(body['room-time'])
#                    exit_time = int(body['exit-time'])
#                    priorityQueue.put((exit_time, seconds))
#                except ValueError:
#                    print("no sound to play")

 #       time.sleep(poll_rate)


def play_sound(total_time_pp):
    hours = int(total_time_pp / 3600)
    minutes = int((total_time_pp % 3600) / 60)
    seconds = int(total_time_pp % 60)

    hours_speech = str(hours) + " hours " if hours != 0 else ''
    mins_speech = str(minutes) + " minutes " if minutes != 0 else ''
    seconds_speech = str(seconds) + " seconds "

    speech = hours_speech + mins_speech + seconds_speech
    print 'about to say: \'' + speech + '\''

    os.system("espeak '" + speech + "' -s " + speed + " -p " + pitch + " -ven-sc+" + variant)

def should_say(last_message,  this_message, last_message_said_at):
    return abs(last_message - this_message) > 2 or time.time() - last_message_said_at > 2.0

#while True:
#    if not priorityQueue.empty():
#        pair = priorityQueue.get()
#
#        if pair[0] - time.time() <= MAX_TIME_PASSED:
#            play_sound(pair[1])
#
#        priorityQueue.task_done()


last_message_said = 0
last_message_said_at = time.time()

while True:
    print 'polling the server...'    

    r = ''
    try:
        r = requests.get(url + '/next_exit_time/' + str(door) + '/')
    except requests.exceptions.ConnectionError:
        print colored('speaker on door: ' + str(door) + ' failed to connect to server', 'yellow')
    else:
        print 'received something from the server: ' + r.text
        if r.text != 'no sound to play':
            time_spent = int(r.text)
            if should_say(last_message_said, time_spent, last_message_said_at):
                play_sound(time_spent)
                last_message = time_spent
                last_message_said_at = time.time()
            else:
                print 'not saying time ' + r.text + ' because it was too similar to a previous one'

    time.sleep(poll_rate)
