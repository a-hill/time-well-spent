from VideoInterface import VideoInterface
import sys
import time
from FaceAlignmentJob import FaceAlignmentJob
import openface

class Main:
    FACE_PREDICTOR = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'

    def __init__(self, door_id, videoInterface, url):
        self.url = url
        self.door_id = door_id
        self.videoInterface = videoInterface
        self.aligner = openface.AlignDlib(self.FACE_PREDICTOR)

    def run(self):
	facesLastFrame = []

        while True:
            # take frame and get time
            frame, t = self.videoInterface.get_frame_and_time()

            if frame is not None:
                # Send frame to another process for alignment
                job = FaceAlignmentJob(frame, t, self.door_id, self.url, self.aligner)
                facesLastFrame = job.run(facesLastFrame)
            else:
                print 'frame is none'

# Arguments - main.py doorNum cameraNum exit/entry
# Main door = 0
if __name__ == '__main__':

    entry_url = 'http://modern-times-1.uksouth.cloudapp.azure.com:5000/submit_face/entry/'
    exit_url = 'http://modern-times-1.uksouth.cloudapp.azure.com:5000/submit_face/exit/'

    #entry_url = 'http://localhost:5000/submit_face/entry/'
    #exit_url = 'http://localhost:5000/submit_face/exit/'

    door_id = int(sys.argv[1])
    camera_id = int(sys.argv[2])

    url = exit_url if sys.argv[3] == 'exit' else entry_url
    # One exit cam and one entry cam per computer
    main = Main(door_id, VideoInterface(camera_id), url)

    # Does not create new process. Anything after this line will not execute
    main.run()
