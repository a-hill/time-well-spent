import cv2
import time

class VideoInterface():

    def __init__(self, cameraIndex=0):
        self.cameraIndex = cameraIndex

    def get_image_from_file(self, path):
        return cv2.imread(path)

    def get_frame(self):
        cap = cv2.VideoCapture(self.cameraIndex)
        if not isinstance(self.cameraIndex, str):
            time.sleep(2) # Allow webcam to wake up
        ret, frame = cap.read()

        if not ret:
            print "Failed to get frame from webcam"
        cap.release()
        return frame