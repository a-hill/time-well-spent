from flask import Flask
import inflect
import pyttsx

app = Flask(__name__)   #Understand what this is?? :/

@app.route('/speaker_time/<int:total_time_pp>/<int:exit_time>')
def get_total_time(total_time_pp, exit_time):
    return play_sound(total_time_pp, exit_time)

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

