import unittest

from VideoInterface import VideoInterface
import numpy as np
import time


class TestVideoInterface(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.DEFAULT_IMAGE_DIMS = 96
        self.TEST_IMAGE_PATH = "../modern-times-test-resources/not-tate/" \
                               "alessio.jpg"
        self.TEST_VIDEO_PATH = "../modern-times-test-resources/not-tate/" \
                               "Abbie3.mov"

    def test_can_read_image_from_file(self):
        image = VideoInterface(self.TEST_IMAGE_PATH)
        test_image = image.get_image_from_file(self.TEST_IMAGE_PATH)
        self.assertIsInstance(test_image, np.ndarray)

    # This test commented out because uses webcam not video so not replicable
    # def test_can_read_frame_from_webcam(self):
    #     video_interface = VideoInterface(0)
    #     frame = video_interface.get_frame()
    #     self.assertIsInstance(frame, np.ndarray)

    def test_can_read_frame_from_video(self):
        video_test_footage = VideoInterface(self.TEST_VIDEO_PATH)
        frame = video_test_footage.get_frame()
        self.assertIsInstance(frame, np.ndarray)
        video_test_footage.destroy_capture()

    def test_can_get_different_frames_from_video(self):
        video_test_footage = VideoInterface(self.TEST_VIDEO_PATH)
        frame1 = video_test_footage.get_frame()
        frame2 = video_test_footage.get_frame()
        self.assertFalse((frame1 == frame2).all())
        video_test_footage.destroy_capture()

    def test_cannot_destroy_capture_for_images(self):
        video_test_footage = VideoInterface(self.TEST_VIDEO_PATH)
        self.assertFalse(video_test_footage.destroy_capture())

    def test_can_get_frames_1_second_apart(self):
        video_test_footage = VideoInterface(self.TEST_VIDEO_PATH)
        frame1 = None
        while frame1 is None:
            frame1, time1 = video_test_footage.get_frame_and_time()

        time.sleep(1)
        frame2 = None
        while frame2 is None:
            frame2, time2 = video_test_footage.get_frame_and_time()

        self.assertIsInstance(frame1, np.ndarray)
        self.assertIsInstance(frame2, np.ndarray)
        self.assertAlmostEqual(time2-time1, 1, 1, None, None)

    # This test commented out because uses webcam not video so not replicable
    # def test_turn_on_both_cameras(self):
    #     entry_cam = VideoInterface(0)
    #     exit_cam = VideoInterface(1)

    #     entry = entry_cam.get_frame()
    #     ex = exit_cam.get_frame()
    #     self.assertIsInstance(entry, np.ndarray,
    #                           "Unable to get frame from entry camera")
    #     self.assertIsInstance(ex, np.ndarray,
    #                        "Unable to get frame from exit camera")
    #     self.assertFalse((entry == ex).all(), "The two frames from" +
    #                      " supposedly different cameras are the same")


if __name__ == '__main__':
    _runner = unittest.TextTestRunner()
    unittest.main(testRunner=_runner)
