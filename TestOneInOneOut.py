import unittest
from VideoInterface import VideoInterface
import numpy as np


class TestOneInOneOut(unittest.TestCase):

    def test_can_read_image_from_file(self):
        pathToFrame = './alessio.jpg'
        videoInterface = VideoInterface()
        testImage = videoInterface.get_image_from_file(pathToFrame)
        self.assertIsInstance(testImage, np.ndarray)

    def test_can_read_frame_from_webcam(self):
        videoInterface = VideoInterface(0)
        frame = videoInterface.get_frame()
        self.assertIsInstance(frame, np.ndarray)

    def test_can_read_frame_from_video(self):
        pathToVideo = "./video.mp4"
        videoInterface = VideoInterface(pathToVideo)
        frame = videoInterface.get_frame()
        self.assertIsInstance(frame, np.ndarray)

    def test_can_create_representation_from_frame(self):
        pass

        # pathToFrame = './test1.jpg'
        # single_file = SingleFile()
        # testImage = single_file.getImageFromFile(pathToFrame)
        # rep = single_file.getRep(testImage)
        # self.assertIsInstance(rep, numpy.ndarray, "Representation created was wrong type; should be array")


if __name__ == '__main__':
    unittest.main()
