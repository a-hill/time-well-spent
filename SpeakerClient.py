import time
import requests
import sys
from termcolor import colored
from Speaker import Speaker

poll_rate = 0.1  # in seconds
url = 'http://modern-times-1.uksouth.cloudapp.azure.com:5000'
door = int(sys.argv[1])
speed = "175"  # Speed in wpm. Default is 175, min is 80, theoretical max 500
pitch = "50"  # Pitch between 0 and 99, default is 50
variant = "m1"  # Can be m1-6 or f1-6 or whisper or croak, not using this!

time_of_last_message_said = 0

print_freq = 20
count = 0

speaker = Speaker()

while True:

    r = ''
    try:
        r = requests.get(url + '/next_exit_time/' + str(door) + '/')
    except requests.exceptions.ConnectionError:
        print colored('speaker on door: ' + str(door) +
                      ' failed to connect to server', 'red')
    else:
        if r.text != 'no sound to play':
            time_spent = int(r.text)
            if speaker.should_say(time_of_last_message_said):
                time_of_last_message_said = time.time()
                speaker.play_sound(time_spent)
            else:
                print colored('Not saying time', 'yellow')
        else:
            if count % print_freq == 0:
                print count, ': no sound to play'
            count += 1

    time.sleep(poll_rate)
