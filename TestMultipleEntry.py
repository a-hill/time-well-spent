import unittest
from FaceAlignmentJob import FaceAlignmentJob
from VideoInterface import VideoInterface
import openface

class TestFacialRecognition(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
        self.pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
        self.testMultipleFaces = "../modern-times-test-resources/not-tate/test_mult.mov"

    def test_can_detect_multiple_faces_in_frame(self):
        videoInterface = VideoInterface(self.testMultipleFaces)
        aligner = openface.AlignDlib(self.pathToDLibFacePredictor)
        # Find a non empty frame,
        # Initially, there are only two faces in the frame
        frame = None
        while frame is None:
            frame, t = videoInterface.get_frame_and_time()

        faceAlignmentJob = FaceAlignmentJob(frame, t, 0, "", aligner)
        facesInRoom = faceAlignmentJob.align_faces()

        print len(facesInRoom)
        self.assertTrue(len(facesInRoom) == 2)


if __name__ == '__main__':
    unittest.main()
