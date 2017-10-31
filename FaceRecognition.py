import cv2
import openface
import numpy as np
from VideoInterface import VideoInterface
import random

class FaceRecognition():

    def __init__(self, facePredictorPath, alignedImageDimensions, networkModelPath):
        self.facePredictorPath = facePredictorPath
        self.alignedImgDimensions = alignedImageDimensions
        self.aligner = openface.AlignDlib(facePredictorPath)
        self.net = openface.TorchNeuralNet(networkModelPath, alignedImageDimensions)

    def get_rep(self, image, imgDim):
        alignedFace = self.align_face(image, imgDim)
        if alignedFace is None: # Alignment failed
            return None
        else:
            rep = self.net.forward(alignedFace)
            return rep

    # private function
    def align_face(self, image, imgDim):
        # Converts image to format expected by aligner
        rgbImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Finds biggest face in frame and gets the box around it
        bb = self.aligner.getLargestFaceBoundingBox(rgbImg)

        if bb is None:  # No face found in frame
            return None

        # Crops and rotates according to bb
        alignedFace = self.aligner.align(imgDim, rgbImg, bb, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

        if alignedFace is None:  # Alignment failed
            return None
        return alignedFace

    def is_same_person(self, rep1, rep2):
        if rep2 is not None and rep1 is not None: # Check they both exist
            d = rep1 - rep2
            distance = np.dot(d, d)
            return distance < 0.99 # This number comes from openface docs
