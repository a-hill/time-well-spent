import unittest
from FaceAlignmentJob import FaceAlignmentJob
from VideoInterface import VideoInterface
import openface


class TestFacialRecognition(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.pathToDLibFacePredictor = './../openface/models/dlib/' + \
                                       'shape_predictor_68_face_landmarks.dat'
        self.pathToTorchNeuralNet = './../openface/models/openface/ ' + \
                                    'nn4.small2.v1.t7'
        self.testMultipleFaces = "../modern-times-test-resources/" + \
                                 "not-tate/test_mult.mov"
        self.testSingleFace = "../modern-times-test-resources" + \
                              "/not-tate/video.mp4"

    def test_can_detect_multiple_faces_in_frame(self):
        video_interface = VideoInterface(self.testMultipleFaces)
        aligner = openface.AlignDlib(self.pathToDLibFacePredictor)
        # Find and run align_faces() on first non empty frame
        frame = None
        while frame is None:
            frame, t = video_interface.get_frame_and_time()

        face_alignment_job = FaceAlignmentJob(frame, t, 0, "", aligner)
        faces_in_room = face_alignment_job.align_faces()

        self.assertTrue(len(faces_in_room) == 2)

    def test_discards_faces_too_small(self):
        video_interface = VideoInterface(self.testSingleFace)
        aligner = openface.AlignDlib(self.pathToDLibFacePredictor)
        # Find and run align_faces() on first non empty frame
        frame = None
        i = 0
        while i < 45:
            frame, t = video_interface.get_frame_and_time()
            i += 1

        if frame is not None:
            face_alignment_job = FaceAlignmentJob(frame, t, 0, "", aligner)
            faces_in_room = face_alignment_job.align_faces()

        self.assertTrue(len(faces_in_room) == 1)


if __name__ == '__main__':
    unittest.main()
