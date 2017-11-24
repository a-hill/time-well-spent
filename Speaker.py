from threading import Thread
import pyttsx
import inflect
from flask import Flask
from Queue import PriorityQueue
from flask import request

queue = PriorityQueue(10)
app = Flask(__name__)

@app.route('/speaker_time/', methods=['POST'])
def get_total_time():
    total_time_pp = request.form['total_time_pp']
    exit_time = request.form['exit_time']
    if total_time_pp is None or exit_time is None:
        print('form not properly submitted to speaker server')
        return 'fail'
    else:
        time_string = get_time_string(int(total_time_pp))
        queue.put((exit_time, time_string))
        return 'success'

def speak(s):
    # sound = pyttsx.init()
    # sound.say(s)
    # sound.runAndWait()
    print(s)

def get_time_string(total_num_seconds):
    hours = int(total_num_seconds / 3600)
    minutes = int((total_num_seconds % 3600) / 60)
    seconds = int(total_num_seconds % 60)
    speak = inflect.engine()
    hours_speech = ""
    mins_speech = ""
    seconds_speech = ""
    if hours > 0:
        s = " "
        if hours > 1:
            s = "s "
        hours_speech = speak.number_to_words(hours) + " hour" + s
    if minutes > 0:
        s = " "
        if minutes > 1:
            s = "s "
        # andd = ""
        # if seconds == 0 and hours > 0:
        #     andd = " and "
        # mins_speech = andd + speak.number_to_words(minutes) + " minute" + s
        mins_speech = speak.number_to_words(minutes) + " minute" + s
    if seconds > 0:
        s = " "
        if seconds > 1:
            s = "s "
        # seconds_speech = "and " + speak.number_to_words(seconds) + " second" + s
        seconds_speech = speak.number_to_words(seconds) + " second" + s
    return hours_speech + mins_speech + seconds_speech


class FlaskThread(Thread):
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)

    def run(self):
        app.run(threaded=True, port=5000, host='0.0.0.0')

class SpeakerThread(Thread):
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)

    def run(self):
        while True:
            sound_to_play = queue.get()
            speak(sound_to_play)
            queue.task_done()


thread1 = FlaskThread()
thread2 = SpeakerThread()

thread1.start()
thread2.start()