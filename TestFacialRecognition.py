import unittest
from FaceRecognition import FaceRecognition
from VideoInterface import VideoInterface
import numpy as np
import time

class TestFacialRecognition(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.defaultImageDims = 96
        self.pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
        self.pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
        self.faceRecognition = FaceRecognition(self.pathToDLibFacePredictor, self.defaultImageDims, self.pathToTorchNeuralNet)
        self.testImagePath = './test_data/alessio.jpg'
        self.andrewImagePath = './test_data/andrew.jpg'
        self.andrewNoBeardImagePath = './test_data/andrew-no-beard.jpg'
        self.testVideoPath = "./test_data/Abbie3.mov"
        self.testVideoSidePath = "./test_data/Abbie4.mov"
        self.testVideoWithGapPath = "./test_data/abbie_with_gap.mov"

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

    def test_can_tell_if_same_person_photos(self):
        videoInterface = VideoInterface()
        frame1 = videoInterface.get_image_from_file(self.andrewNoBeardImagePath)
        frame2 = videoInterface.get_image_from_file(self.andrewImagePath)
        rep1 = self.faceRecognition.get_rep(frame1, self.defaultImageDims)
        rep2 = self.faceRecognition.get_rep(frame2, self.defaultImageDims)
        self.assertTrue(self.faceRecognition.is_same_person(rep1, rep2))

    def test_can_detect_face_from_video(self):
        videoInterface = VideoInterface(self.testVideoPath)
        # loop until it sees a face
        rep = None
        i = 0
        while rep is None:
            frame = videoInterface.get_frame()
            if (frame is not None):
                rep = self.faceRecognition.get_rep(frame, self.defaultImageDims)
                i = i + 1
        self.assertTrue(i == 1) # It should find a face in the first frame
        self.assertIsInstance(rep, np.ndarray)

    # This test commented out because doesn't work
    # def test_can_detect_face_from_video_side_angle(self):
    #     videoInterface = VideoInterface(self.testVideoSidePath)
    #     # loop until it sees a face
    #     rep = None
    #     i = 0
    #     while rep is None:
    #         frame = videoInterface.get_frame()
    #         if (frame is not None):
    #             rep = self.faceRecognition.get_rep(frame, self.defaultImageDims)
    #             i = i + 1
    #     print(i)
    #     self.assertIsInstance(rep, np.ndarray)

    # This test commented out because uses webcam not video so not replicable easily
    # def test_can_detect_face_from_webcam(self):
    #     videoInterface = VideoInterface(0)
    #     # loop until it sees a face
    #     rep = None
    #     while rep is None:
    #         frame = videoInterface.get_frame()
    #         if (frame is not None):
    #             rep = self.faceRecognition.get_rep(frame, self.defaultImageDims)
    #     self.assertIsInstance(rep, np.ndarray)

    # This test is broken because of the video interface cap bug (new cap each frame)
    # def test_can_do_time_difference_video(self):
    #     videoInterface = VideoInterface(self.testVideoWithGapPath)
    #     rep1 = None
    #     while rep1 is None:
    #         frame, time1 = videoInterface.get_frame_and_time()
    #         rep1 = self.faceRecognition.get_rep(frame, self.defaultImageDims)

    #     time.sleep(1)
    #     samePerson = False
    #     while not samePerson:
    #        # obtain and save second face
    #        frame2, time2 = videoInterface.get_frame_and_time()
    #        rep2 = self.faceRecognition.get_rep(frame2, self.defaultImageDims)
    #        samePerson = (self.faceRecognition.is_same_person(rep1, rep2))
    #     self.assertTrue(1.33 <= (time2-time1) <= 1.34)



if __name__ == '__main__':
    unittest.main()