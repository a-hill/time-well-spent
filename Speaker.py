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

def play_sound(total_time_pp, exit_time):
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
    #sound = pyttsx.init()
    #sound.say(speech)
    #sound.runAndWait()

#if __name__ == "__main__":
#    app.run(threaded=True, host='0.0.0.0')

