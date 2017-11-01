import cv2
import openface
import numpy as np
from VideoInterface import VideoInterface
import random


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
            return None
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

        if alignedFace is None:  # Alignment failed
            return None
        return alignedFace

    #private function
    def align_faces(self, image):
        # Converts image to format expected by aligner
        rgbImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        faces = self.aligner.getAllFaceBoundingBoxes(rgbImg)

        # No face found in frame
        if len(faces) == 0:
            return None

        alignedFaces = []
        # Crops and rotates each bounding box in the frame
        for face in faces:
            aligned = self.aligner.align(self.DEFAULT_IMAGE_DIMENSION, rgbImg, face,
                                         landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            if aligned is not None:
                alignedFaces.append(aligned)

        return alignedFaces

    def is_same_person(self, rep1, rep2):
        if rep2 is not None and rep1 is not None:  # Check they both exist
            d = rep1 - rep2
            distance = np.dot(d, d)
            return distance < 0.99  # This number comes from openface docs
