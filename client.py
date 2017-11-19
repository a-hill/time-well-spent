from VideoInterface import VideoInterface
import FaceAlignmentJob
import time

class Client:
    MAX_FRAMERATE = 0.2 # five frames per second

    def __init__(self, door, cameras):
        self.door = door
        self.cameras = cameras

    def run(self):
        while True:
            start = time.clock()

            # get frame from one camera only for load balancing reasons
            for camera in self.cameras:
                frame, t = camera[0].get_frame_and_time()
                FaceAlignmentJob(frame, t, self.door, camera[1])

            #rate limiting
            delta = (time.clock() - start) * 1000
            if delta < self.MAX_FRAMERATE:
                time.sleep(self.MAX_FRAMERATE - delta)

client = Client('TODO', [
    [VideoInterface(0), "entry"],
    [VideoInterface(1), "exit"]
])
client.run()
