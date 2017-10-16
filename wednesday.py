import time
import argparse
import itertools
import cv2
import os

import numpy as np
np.set_printoptions(precision=2)

import openface

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

# Figure out how to delete this
parser = argparse.ArgumentParser()

#parser.add_argument('imgs', type=str, nargs='+', help="Input images.")
parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,
                    help="Default image dimension.", default=96)
parser.add_argument('--verbose', action='store_true')

args = parser.parse_args()
# END of needs deleting


start = time.time()
difference = time.time() - start

align = openface.AlignDlib(args.dlibFacePredictor)
net = openface.TorchNeuralNet(args.networkModel, args.imgDim)

# Get Representation of image
# Method mostly taken from demo file from openface
def getRep(imgPath):
    # if args.verbose:
    #    print("Processing {}.".format(imgPath))

    # Image Import
    bgrImg = cv2.imread(imgPath)
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    #if args.verbose:
    #    print("  + Original size: {}".format(rgbImg.shape))

    # Face Detection
    start = time.time()
    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        #raise Exception("Unable to find a face: {}".format(imgPath))
        return None

    #if args.verbose:
    #    print("  + Face detection took {} seconds.".format(time.time() - start))

    # Image Alignment
    start = time.time()
    alignedFace = align.align(args.imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image: {}".format(imgPath))
    #if args.verbose:
    #    print("  + Face alignment took {} seconds.".format(time.time() - start))

    # Openface pass
    start = time.time()
    rep = net.forward(alignedFace)

    #if args.verbose:
    #    print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
    #    print("Representation:")
    #    print(rep)
    #    print("-----\n")
    return rep

img1 = 'images/alessio.jpg'
img2 = 'images/andrew1.jpg'

# On entry
rep1 = getRep(img1)
while rep1 is None:
    # Get Next Image
    rep1 = getRep(img1)

# On Exit
rep2 = getRep(img2)
while rep2 is None:
    # Get Next Image
    rep2 = getRep(img2)

d = rep1 - rep2

distance = np.dot(d, d)

print(distance)