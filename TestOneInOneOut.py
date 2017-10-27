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
        self.testImagePath = './test_data/alessio.jpg'
        self.andrewImagePath = './test_data/andrew.jpg'
        self.testVideoPath = "./test_data/video.mp4"


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

    def test_can_tell_people_apart_photos(self):
        videoInterface = VideoInterface()
        frame1 = videoInterface.get_image_from_file(self.testImagePath)
        frame2 = videoInterface.get_image_from_file(self.andrewImagePath)
        rep1 = self.faceRecognition.get_rep(frame1, self.defaultImageDims)
        rep2 = self.faceRecognition.get_rep(frame2, self.defaultImageDims)
        self.assertFalse(self.faceRecognition.is_same_person(rep1, rep2))


if __name__ == '__main__':
    unittest.main()
