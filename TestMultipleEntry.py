import unittest
from FaceRecognition import FaceRecognition
from VideoInterface import VideoInterface
import cv2


class TestFacialRecognition(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
        self.pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
        self.faceRecognition = FaceRecognition(self.pathToDLibFacePredictor, self.pathToTorchNeuralNet)
        self.testSingleFilePath = "./test_data/tate-1/angle1-threefacessinglefile.mov"
        self.testStoreOneFace = "./test_data/tate-1/angle1-oneface.mov"


    # def test_can_store_face_on_entrace(self):
    #     videoInterface = VideoInterface(self.testStoreOneFace)
    #     face_reps = []
    #     frame = "Nonsense"
    #     duplicate = False
    #     while frame is not None:
    #         frame = videoInterface.get_frame()
    #         if frame is not None:
    #             currentRep = self.faceRecognition.get_rep(frame)
    #             if currentRep is not None:
    #                 for f in face_reps:
    #                     if self.faceRecognition.is_same_person(currentRep, f):
    #                         duplicate = True
    #                         break
    #                     else:
    #                         duplicate = False
    #                 if not duplicate:
    #                     face_reps.append(currentRep)
    #     print (len(face_reps))
    #     self.assertTrue(len(face_reps) == 1)


    def test_can_store_multiple_faces_on_entrance(self):
        video_interface = VideoInterface(self.testSingleFilePath)
        reps = []
        f = "Nonsense"
        while f is not None:
            f = video_interface.get_frame()
            if f is not None:
                all_faces = self.faceRecognition.get_reps(f)
                if len(all_faces) > 0:
                    for face in all_faces:
                        already_exists_in_list = self.find_face_in_list(reps, face)
                        if not already_exists_in_list:
                            reps.append(face)
        print len(reps)
        self.assertTrue(len(reps) == 3)


    def find_face_in_list(self, reps, face):
            for r in reps:
                if self.faceRecognition.is_same_person(face, r):
                    return True
            return False


if __name__ == '__main__':
    unittest.main()
