import time
import argparse
import itertools
import os
import pyttsx
import numpy as np
import cv2
import random
np.set_printoptions(precision=2)

import openface

class Main:
    DEFAULT_IMAGE_DIMENSION = 96

    def __init__(self):
        random.seed()
        self.facesInRoom = []

        # Gets path of where you are now
        fileDir = os.path.dirname(os.path.realpath(__file__))
        modelDir = os.path.join(fileDir, '..', 'openface', 'models')
        dlibModelDir = os.path.join(modelDir, 'dlib')
        openfaceModelDir = os.path.join(modelDir, 'openface')
        self.DEFAULT_NETWORK_MODEL = os.path.join(openfaceModelDir, 'nn4.small2.v1.t7')
        self.DEFAULT_FACE_PREDICTOR = os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat")


        self.align = openface.AlignDlib(self.DEFAULT_FACE_PREDICTOR)
        self.net = openface.TorchNeuralNet(self.DEFAULT_NETWORK_MODEL, self.DEFAULT_IMAGE_DIMENSION)
        self.cap = cv2.VideoCapture(0)

        self.a1 = cv2.imread("a1.jpg")
        self.a2 = cv2.imread("a2.jpg")
        self.b1 = cv2.imread("b1.jpg")
        self.b2 = cv2.imread("b2.jpg")
        self.blue = cv2.imread("blue.jpg")

    def getVectorRep(self, bgrImg):
        # takes in an image (not an image path!)
        # returns a vector representation of the largest face found in a photo
        # returns None if no face found or was unable to align
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

        bb = self.align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            #no face found
            return None

        alignedFace = self.align.align(self.DEFAULT_IMAGE_DIMENSION, rgbImg, bb, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            #unable to align face
            return None

        rep = self.net.forward(alignedFace)

        return rep

    def faceMatch(self, a, b):
        if len(a) != len(b):
            return False

        # takes in two vectors, returns a boolean if the faces they represent match
        distance = a - b
        squaredl2 = np.dot(distance, distance)

        return squaredl2 < 1.0

    def addFaceToRoom(self, rep):
        if not any([self.faceMatch(face, rep) for [face, t] in self.facesInRoom]):
            self.facesInRoom.append([rep, time.time()])

    def removeFaceFromRoom(self, rep):
        newFacesInRoom = []
        for face in self.facesInRoom:
            if self.faceMatch(face[0], rep):
                print("This face was in the room for: ", time.time() - face[1])
            else:
                newFacesInRoom.append(face)
        self.facesInRoom = newFacesInRoom

    def getEnterCameraImage(self):
        # TODO: replace this with input from a camera
        r = random.random()
        if r < 0.25:
            return self.a1
        elif r < 0.5:
            return self.a2
        elif r < 0.75:
            return self.b1
        else:
            return self.b2

    def getExitCameraImage(self):
        # TODO: replace this with input from another camera
        return self.getEnterCameraImage()

    def run(self):
        quit = False
        while not quit:
            t = time.time()

            # check for people leaving
            image = self.getExitCameraImage()
            rep = self.getVectorRep(image)

            if rep is not None:
                self.removeFaceFromRoom(rep)

            # check for people entering
            image = self.getEnterCameraImage()
            rep = self.getVectorRep(image)

            if rep is not None:
                self.addFaceToRoom(rep)

            print("This tick took ", time.time() - t, " seconds to run")
            print("Ther are ", len(self.facesInRoom), " people in the room")

        self.cap.release()

main = Main()
main.run()
