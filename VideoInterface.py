import cv2
import time
import subprocess

class VideoInterface():
    def __init__(self, captureNo):
        self.captureNo = captureNo
        self.capture = None

    def make_capture(self):
        self.capture = cv2.VideoCapture(self.captureNo)
        self.setup_camera()

    def setup_camera(self):
        self.set_variable('focus_auto', 0)
        self.set_variable('focus_absolute', 0)

    def set_variable(self, variable, value):
        subprocess.check_call(
            "v4l2-ctl -d /dev/video" + str(self.captureNo) +
            ' -c ' + variable + "=" + str(value), shell=True
        )

    def get_image_from_file(self, path):
        return cv2.imread(path)

    def get_frame(self):
        if self.capture is None:
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
