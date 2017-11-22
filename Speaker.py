from threading import Thread
import pyttsx
import inflect
from flask import Flask
from Queue import PriorityQueue

queue = PriorityQueue(10)
app = Flask(__name__)

@app.route('/speaker_time/', methods=['POST'])
def get_total_time():
    total_time_pp = Flask.request.form['total_time_pp']
    exit_time = Flask.request.form['exit_time']

    if total_time_pp is None or exit_time is None:
        print('form not properly submitted to speaker server')
        return 'fail'
    else:
        time_string = get_time_string(int(total_time_pp))
        queue.put((exit_time, time_string))
        return 'success'


class Speaker(Thread):
    def run(self):
        global queue
        while True:
            sound_to_play = queue.get()
            self.speak(sound_to_play)
            queue.task_done()

    def speak(self, s):
        sound = pyttsx.init()
        sound.say(s)
        sound.runAndWait()


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

if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0')
    Speaker().start()