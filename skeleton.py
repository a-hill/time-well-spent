# this is a skeleton program millie wrote
# an outline of what a single threaded solution might look like
# doesnt compile!

import cv2

import numpy as np
np.set_printoptions(precision=2)

import openface

class Skeleton:
    def setup(self):
        self.align = openface.AlignDlib(????????) #TODO
        self.net = openface.TorchNeuralNet(??????????, ????????) #TODO

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

    def run(self):
        facesInRoom = []

        quit = False
        while not quit:
            # check for people entering
            image = getEnterCameraImage() #TODO
            rep = getVectorRep(image)

            if rep is not None and not any([faceMatch(x, rep) for x in facesInRoom]):
                facesInRoom.append(rep)

            # check for people leaving
            image = getExitCameraImage() #TODO
            rep = getVectorRep(image)

            if rep is not None:
                facesInRoom = [x for x in facesInRoom if not faceMatch(x, rep)]

skeleton = Skeleton()
skeleton.setup()
skeleton.run()
