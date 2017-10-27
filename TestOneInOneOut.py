import unittest

from FaceRecognition import FaceRecognition
from VideoInterface import VideoInterface
import numpy as np


class TestOneInOneOut(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.defaultImageDims = 96
        self.pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
        self.pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
        self.faceRecognition = FaceRecognition(self.pathToDLibFacePredictor, self.defaultImageDims, self.pathToTorchNeuralNet)
        self.testImagePath = './alessio.jpg'
        self.testVideoPath = "./video.mp4"


    def test_can_read_image_from_file(self):
        videoInterface = VideoInterface()
        testImage = videoInterface.get_image_from_file(self.testImagePath)
        self.assertIsInstance(testImage, np.ndarray)

    def test_can_read_frame_from_webcam(self):
        videoInterface = VideoInterface(0)
        frame = videoInterface.get_frame()
        self.assertIsInstance(frame, np.ndarray)

    def test_can_read_frame_from_video(self):
        videoInterface = VideoInterface(self.testVideoPath)
        frame = videoInterface.get_frame()
        self.assertIsInstance(frame, np.ndarray)

    def test_can_create_representation_from_frame(self):
        videoInterface = VideoInterface()
        frame = videoInterface.get_image_from_file(self.testImagePath)
        faceRepresentation = self.faceRecognition.get_rep(frame, self.defaultImageDims)
        self.assertIsInstance(faceRepresentation, np.ndarray, "Representation created was wrong type; should be array")


if __name__ == '__main__':
    unittest.main()
