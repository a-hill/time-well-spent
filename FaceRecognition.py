import cv2
import openface
import numpy as np
from VideoInterface import VideoInterface


class FaceRecognition():
    DEFAULT_IMAGE_DIMENSION = 96

    def __init__(self, facePredictorPath, networkModelPath):
        self.facePredictorPath = facePredictorPath
        self.aligner = openface.AlignDlib(facePredictorPath)
        self.net = openface.TorchNeuralNet(networkModelPath, self.DEFAULT_IMAGE_DIMENSION)

    def get_rep(self, image):
        alignedFace = self.align_face(image)
        if alignedFace is None:  # Alignment failed
            return None
        else:
            rep = self.net.forward(alignedFace)
            return rep

    def get_reps(self, image):
        faces = self.align_faces(image)
        if len(faces) == 0:  # Alignment failed
            return []
        else:
            reps = []
            for face in faces:
                reps.append(self.net.forward(face))
            return reps

    # private function
    def align_face(self, image):
        # Converts image to format expected by aligner
        rgbImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Finds biggest face in frame and gets the box around it
        bb = self.aligner.getLargestFaceBoundingBox(rgbImg)

        if bb is None:  # No face found in frame
            return None

        # Crops and rotates according to bb
        alignedFace = self.aligner.align(self.DEFAULT_IMAGE_DIMENSION, rgbImg, bb,
                                         landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

        return alignedFace

    #private function
    def align_faces(self, image):
        # Converts image to format expected by aligner
        rgbImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        faces = self.aligner.getAllFaceBoundingBoxes(rgbImg)
        #remove smallest box from list of faces before alignment
        # if (len(faces) > 0) or len(faces) == 1:
        #     smallest = min(faces, key=lambda rect: rect.width() * rect.height())


        # No face found in frame
        if len(faces) == 0:
            return []

        alignedFaces = []
        # Crops and rotates each bounding box in the frame
        for face in faces:
            aligned = self.aligner.align(self.DEFAULT_IMAGE_DIMENSION, rgbImg, face,
                                         landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            if aligned is not None:
                alignedFaces.append(aligned)

        return alignedFaces

    @staticmethod
    def is_same_person(rep1, rep2):
        if rep2 is not None and rep1 is not None: # Check they both exist
            if len(rep1) != len(rep2): # Check they're same length
                return False
            d = rep1 - rep2
            distance = np.dot(d, d)
            return distance < 0.99  # This number comes from openface docs
        else:
            return False
