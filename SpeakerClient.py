import time
import requests
import sys
from termcolor import colored
from Speaker import Speaker

_POLL_RATE = 0.1  # in seconds
_URL = 'http://modern-times-1.uksouth.cloudapp.azure.com:5000'
_door = int(sys.argv[1])

_time_of_last_message_said = 0

_PRINT_FREQ = 20
_count = 0

_speaker = Speaker()

while True:

    r = ''
    try:
        r = requests.get(_URL + '/next_exit_time/' + str(_door) + '/')
    except requests.exceptions.ConnectionError:
        print colored('speaker on door: ' + str(_door) +
                      ' failed to connect to server', 'red')
    else:
        if r.text != 'no sound to play':
            _time_spent = int(r.text)
            if _speaker.should_say(_time_of_last_message_said):
                _time_of_last_message_said = time.time()
                _speaker.play_sound(_time_spent)
            else:
                print colored('Not saying time', 'yellow')
        else:
            if _count % _PRINT_FREQ == 0:
                print _count, ': no sound to play'
            _count += 1

    time.sleep(_POLL_RATE)
