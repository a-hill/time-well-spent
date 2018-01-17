import cv2
import time
import subprocess


class VideoInterface:
    def __init__(self, capture_num):
        self.capture_num = capture_num
        self._capture = None
        # Set filePath for reading from video file
        # If reading from video, setup_camera() must not be called
        if isinstance(capture_num, str):
            self._reading_from_video_file = True
        else:
            self._reading_from_video_file = False

    def make_capture(self):
        self._capture = cv2.VideoCapture(self.capture_num)
        if not self._reading_from_video_file:
            self.setup_camera()

    def setup_camera(self):
        self.set_variable('focus_auto', 0)
        self.set_variable('focus_absolute', 0)
        self.set_variable('exposure_auto', 1)
        self.set_variable('exposure_absolute', 250)

    def set_variable(self, variable, value):
        subprocess.check_call(
            "v4l2-ctl -d /dev/video" + str(self.capture_num) +
            ' -c ' + variable + "=" + str(value), shell=True
        )

    @staticmethod
    def get_image_from_file(path):
        return cv2.imread(path)

    def get_frame(self):
        if self._capture is None:
            self.make_capture()

        ret, frame = self._capture.read()

        if not ret:
            print "Failed to get frame from video stream"
            frame = None  # Check what's returned when reached end of video
        return frame

    def get_frame_and_time(self):
        frame = self.get_frame()
        t = time.time()
        return frame, t

    def destroy_capture(self):
        if self._capture is not None:
            self._capture.release()
            return True
        return False
