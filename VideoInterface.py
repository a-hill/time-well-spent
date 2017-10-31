import cv2
import time

class VideoInterface():

    def __init__(self, videoSource=0):
        self.videoSource = videoSource

    def get_image_from_file(self, path):
        return cv2.imread(path)

    def get_frame(self):
        cap = cv2.VideoCapture(self.videoSource)
        if not isinstance(self.videoSource, str):
            time.sleep(2) # Allow webcam to wake up
        ret, frame = cap.read()

        if not ret:
            print "Failed to get frame from video stream"
            frame = None # Check what this returns when reaching the end of video
        cap.release()
        return frame