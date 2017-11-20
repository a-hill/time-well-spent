from flask import Flask
import inflect
import pyttsx

app = Flask(__name__)   #Understand what this is?? :/

@app.route('/speaker_time/', methods=['POST'])
def get_total_time():
    total_time_pp = request.form['total_time_pp']
    exit_time = request.form['exit_time']

    if total_time_pp is None or exit_time is None:
        print('form not properly submitted to speaker server')
        return 'fail'
    else:
        play_sound(int(total_time_pp), int(exit_time))
        return 'success'

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

def add_to_queue(total_time_pp, exit_time):
    

def play_sound(total_time_pp, exit_time):
    speech = get_time_string(total_time_pp)
    print speech
    #sound = pyttsx.init()
    #sound.say(speech)
    #sound.runAndWait()

if __name__ == "__main__":
    play_sound(0, 50)
#    app.run(threaded=True, host='0.0.0.0')

