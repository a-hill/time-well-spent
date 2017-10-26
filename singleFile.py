import time
import argparse
import itertools
import cv2
import os
import pyttsx
import numpy as np
np.set_printoptions(precision=2)

import openface

#Gets path of where you are now
fileDir = os.path.dirname(os.path.realpath(__file__))
print (fileDir)

modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
print(dlibModelDir)
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

align = openface.AlignDlib(args.dlibFacePredictor)
net = openface.TorchNeuralNet(args.networkModel, args.imgDim)

# Get Representation of image
# Method mostly taken from demo file from openface
def getRep(image):
    # if args.verbose:
    #    print("Processing {}.".format(imgPath))

    # Image Import
    #bgrImg = cv2.imread(imgPath)
    bgrImg = image
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    #if args.verbose:
    #    print("  + Original size: {}".format(rgbImg.shape))

    # Face Detection
    #start = time.time()
    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        #raise Exception("Unable to find a face: {}".format(imgPath))
        return None

    #if args.verbose:
    #    print("  + Face detection took {} seconds.".format(time.time() - start))

    # Image Alignment
    #start = time.time()
    alignedFace = align.align(args.imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image: {}".format(imgPath))
    #if args.verbose:
    #    print("  + Face alignment took {} seconds.".format(time.time() - start))

    # Openface pass
    # start = time.time()
    rep = net.forward(alignedFace)

    #if args.verbose:
    #    print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
    #    print("Representation:")
    #    print(rep)
    #    print("-----\n")
    return rep

def checkIfSamePerson(rep1, rep2):
    if rep2 is not None and rep1 is not None:
        d = rep1 - rep2
        distance = np.dot(d, d)
        print('')
        print('Distance:')
        print distance
        return distance < 0.99

#img1 = 'images/alessio.jpg'
#img2 = 'images/andrew1.jpg'

# Set-up video feed
cap = cv2.VideoCapture(0)

faces = []
# On entry

#Get vector representation of frame, will keep running until face detected
#Simulates database, will currently only hold two faces
while len(faces) < 2:
    # Get Next Image
    ret, frame = cap.read()
    entry_time = time.time()

    t = time.time()
    rep1 = getRep(frame)
    l = time.time() - t
    print("It took ", l, " seconds to process that")
    if rep1 is not None:
        #Before appending, check if duplicate exists
        if len(faces) > 0:
            for f in faces:
                if not checkIfSamePerson(f[0], rep1):
                    print 'Added a face'
                    a_face = (rep1, entry_time);
                    faces.append(a_face)
                else:
                    print 'Duplicate found'

        else:
            print'initial case'
            a_face = (rep1, entry_time);
            faces.append(a_face)




print 'entry representation formed, sleeping'
# Close video stream
cap.release()
#waiting for user input to take next image instead of sleeping
raw_input("Press enter to capture again")

print 'waking up'

# Set-up video feed
cap = cv2.VideoCapture(0)
# On exit
#ret, frame = cap.read()
#time_difference = time.time() - entry_time
#rep2 = getRep(frame)
i = 0
while True:
    # Get Next Image
    ret, frame = cap.read()
    rep2 = getRep(frame)
    if rep2 is not None:
        for f in faces:
            if checkIfSamePerson(f[0], rep2):
                print 'Faces found = ' + str(i)
                i = i + 1
                print ('Your Time: ')
                time_difference = time.time() - f[1]
                print(time_difference)
                faces.remove(f)
    if len(faces) == 0:
        print 'Found all faces, breaking out'
        break


# Close video stream
cap.release()

#print 'exit representation formed'

#print('Time:This is currently wrong!')
#print(time_difference)

#os.system('say ' + str(int(time_difference) // 60) + ' minutes and ' + str(round(time_difference, 2) % 60) + ' seconds')
