import unittest

from VideoInterface import VideoInterface
import numpy as np
import time
import cv2

class TestOneInOneOut(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.defaultImageDims = 96
        self.testImagePath = './test_data/alessio.jpg'
        self.testVideoPath = "./test_data/Abbie3.mov"

    def test_can_read_image_from_file(self):
        image = VideoInterface(self.testImagePath)
        testImage = image.get_image_from_file(self.testImagePath)
        self.assertIsInstance(testImage, np.ndarray)

    # This test commented out because uses webcam not video so not replicable easily
    # def test_can_read_frame_from_webcam(self):
    #     videoInterface = VideoInterface(0)
    #     frame = videoInterface.get_frame()
    #     self.assertIsInstance(frame, np.ndarray)

    def test_can_read_frame_from_video(self):
        videoAbbie = VideoInterface(self.testVideoPath)
        frame = videoAbbie.get_frame()
        self.assertIsInstance(frame, np.ndarray)
        videoAbbie.destroy_capture()

    def test_can_get_different_frames_from_video(self):
        videoAbbie = VideoInterface(self.testVideoPath)
        frame1 = videoAbbie.get_frame()
        frame2 = videoAbbie.get_frame()
        self.assertFalse((frame1 == frame2).all())
        videoAbbie.destroy_capture()

    def test_cannot_destroy_capture_for_images(self):
        videoAbbie = VideoInterface(self.testVideoPath)
        self.assertFalse(videoAbbie.destroy_capture())

    def test_can_get_frames_1_second_apart(self):
        videoAbbie = VideoInterface(self.testVideoPath)
        frame1 = None
        while frame1 is None:
            frame1, time1 = videoAbbie.get_frame_and_time()

        time.sleep(1)
        frame2 = None
        while frame2 is None:
            frame2, time2 = videoAbbie.get_frame_and_time()

        self.assertIsInstance(frame1, np.ndarray)
        self.assertIsInstance(frame2, np.ndarray)
        self.assertAlmostEqual(time2-time1, 1, 1, None, None)



if __name__ == '__main__':
    unittest.main()
