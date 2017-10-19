# this is a skeleton program millie wrote
# an outline of what a single threaded solution might look like
# doesnt compile!

import cv2

import numpy as np
np.set_printoptions(precision=2)

import openface

class Skeleton:
    def __init__(self):
        self.facesInRoom = []

        # TODO: set up these things properly
        self.align = openface.AlignDlib(????????) #TODO
        self.net = openface.TorchNeuralNet(??????????, ????????) #TODO
        self.cap = cv2.VideoCapture(0)

    def getVectorRep(self, bgrImg):
        # takes in an image (not an image path!)
        # returns a vector representation of the largest face found in a photo
        # returns None if no face found or was unable to align
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

        bb = align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            #no face found
            return None

        alignedFace = align.align(args.imgDim, rgbImg, bb, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            #unable to align face
            return None

        rep = net.forward(alignedFace)

        return rep

    def faceMatch(self, a, b):
        # takes in two vectors, returns a boolean if the faces they represent match
        distance = a - b
        squaredl2 = np.dot(distance, distance)

        return squaredl2 < 1.0

    def addFaceToRoom(self, rep):
        # TODO: replace with database access
        if not any([faceMatch(x, rep) for x in facesInRoom]):
            facesInRoom.append([rep, time.time()])

    def removeFaceFromRoom(self, rep):
        # TODO: replace with database access
        newFacesInRoom = []
        for face in facesInRoom:
            if faceMatch(face[0], rep):
                print("This face was in the room for: ", time.time() - face[1])
            else:
                newFacesInRoom.append(face)
        facesInRoom = newFacesInRoom

    def getEnterCameraImage(self):
        # TODO: replace this with input from a camera
        ret, frame = cap.read()
        return frame

    def getExitCameraImage(self):
        # TODO: replace this with input from another camera
        ret, frame = cap.read()
        return frame

    def run(self):
        quit = False
        while not quit:
            # check for people entering
            image = getEnterCameraImage()
            rep = getVectorRep(image)

            if rep is not None:
                addFaceToRoom(rep)

            # check for people leaving
            image = getExitCameraImage()
            rep = getVectorRep(image)

            if rep is not None:
                removeFaceFromRoom(rep)

        cap.release()

skeleton = Skeleton()
skeleton.run()
