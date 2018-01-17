import time
import os
from termcolor import colored
from gtts import gTTS


class Speaker:
    def __init__(self):
        pass

    def play_sound(self, total_time_pp):
        speech = self.seconds_to_string(total_time_pp)
        print colored('about to say: \'' + speech + '\'', 'green')

        tts = gTTS(text=speech, lang='en')
        filename = 'temp.mp3'
        tts.save(filename)
        time.sleep(0.1)

        try:
            os.system(
                'cvlc ' + filename + ' --play-and-exit >/dev/null 2>/dev/null')
            os.remove(filename)
        except:
            print colored('WARNING OS ERROR IN SPEAKER', 'red')

    @staticmethod
    def seconds_to_string(total_time_pp):
        hours = int(total_time_pp / 3600)
        minutes = int((total_time_pp % 3600) / 60)
        seconds = int(total_time_pp % 60)

        hours_speech = str(hours) + " hours " if hours != 0 else ''
        mins_speech = str(minutes) + " minutes " if minutes != 0 else ''
        seconds_speech = str(seconds) + " seconds " if seconds != 0 else ''

        speech = hours_speech + mins_speech + seconds_speech
        return speech

    @staticmethod
    def should_say(last_message):
        return abs(last_message - time.time()) > 5
