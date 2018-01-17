from videointerface import VideoInterface
import sys
from facealignmentjob import FaceAlignmentJob
import openface


class Main:
    _FACE_PREDICTOR = \
        './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'

    def __init__(self, door_id, video_interface, url):
        self.url = url
        self.door_id = door_id
        self.video_interface = video_interface
        self.aligner = openface.AlignDlib(self._FACE_PREDICTOR)

    def run(self):
        while True:
            # take frame and get time
            frame, t = self.video_interface.get_frame_and_time()

            if frame is not None:
                # Send frame to another process for alignment
                job = FaceAlignmentJob(frame, t, self.door_id, self.url,
                                       self.aligner)
                job.run()
            else:
                print 'frame is none'


# Arguments - main.py doorNum cameraNum exit/entry
# Main door = 0
if __name__ == '__main__':

    _BASE_URL = 'http://modern-times-1.uksouth.cloudapp.azure.com:5000/'

    _entry_url = _BASE_URL + 'submit_face/entry/'
    _exit_url = _BASE_URL + 'submit_face/exit/'

    _door_id = int(sys.argv[1])
    _camera_id = int(sys.argv[2])

    _url = _exit_url if sys.argv[3] == 'exit' else _entry_url
    # One exit cam and one entry cam per computer
    _main = Main(_door_id, VideoInterface(_camera_id), _url)

    # Does not create new process. Anything after this line will not execute
    _main.run()
