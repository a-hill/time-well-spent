from VideoInterface import VideoInterface
import sys
import time
from FaceAlignmentJob import FaceAlignmentJob


class Main:
    def __init__(self, door_id, videoInterface, url):
        self.url = url
        self.door_id = door_id
        self.MAX_FRAMERATE = 0.5  # 2 frames per second
        self.videoInterface = videoInterface

    def run(self):
        while True:
            # start rate limiting
            start = time.clock()

            # take frame and get time
            frame, t = self.videoInterface.get_frame_and_time()

            # todo: if frame is none????
            if frame is not None:
                # Send frame to another process for alignment
                job = FaceAlignmentJob(frame, t, door_id, url)
                job.process.start()
            else:
                print 'frame is none'

            # rate limiting
            delta = time.clock() - start
            if delta < self.MAX_FRAMERATE:
                time.sleep(self.MAX_FRAMERATE - delta)


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
