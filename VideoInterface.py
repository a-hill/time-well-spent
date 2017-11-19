import cv2
import time

class VideoInterface():

    def __init__(self, capturePath):
        self.capturePath = capturePath
        self.capture = None

    def make_capture(self):
        self.capture = cv2.VideoCapture(self.capturePath)

    def get_image_from_file(self, path):
        return cv2.imread(path)

    def get_frame(self):
        if self.capture == None:
            self.make_capture()

        ret, frame = self.capture.read()

        if not ret:
            print "Failed to get frame from video stream"
            frame = None # Check what this returns when reaching the end of video
        return frame

    def get_frame_and_time(self):
        frame = self.get_frame()
        t = time.time()
        return frame, t

    def destroy_capture(self):
        if self.capture is not None:
            self.capture.release()
            return True
        return False
