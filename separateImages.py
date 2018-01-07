import os
import cv2
import openface
import numpy as np

def separate(door_dir):
    #Go through each image in door_dir
    i = 1
    for fname in os.listdir(door_dir):
        if fname != ".DS_Store" and fname != "1512216490-entry-1.jpg":
            print "onto new person"
            #Create new directory for each image
            newDirName = "Person" + str(i)
            os.mkdir("./separated_door1/" + newDirName)
            #Go through each image and search for match in all 4 directories
            findMatch(dirA, newDirName, fname)
            findMatch(dirB, newDirName, fname)
            findMatch(dirC, newDirName, fname)
            findMatch(dirD, newDirName, fname)
            i+=1


def getRep(img):
    #img should already be in bgr
    if img is not None:
        rep = net.forward(img)
        return rep
    else:
        return None


def faceMatch(repEn, repEx):
    if repEn is None or repEx is None:
        return False

    if len(repEn) != len(repEx):  # Check they're same length
        return False

    d = repEn - repEx
    dot = np.dot(d, d)
    return dot < 0.99


def findMatch(searchDir, personDir, origFName):
    #Check if the given image matches any in searchDir
    for fname in os.listdir(searchDir):
        #only check exit images
        if "exit" in fname:
            #Get the time and compare against entry
            splitFName = fname.split("-")
            exitTime = int(splitFName[0])
            splitOrigName = origFName.split("-")
            entryTime = int(splitOrigName[0])
            if exitTime > entryTime:
                rgbEntry = cv2.imread("/Users/riajha/modern-times-server/door1/" + origFName, 1)
                bgrExit =  cv2.imread(searchDir + "/"+fname, 1)
                imEntry = cv2.cvtColor(rgbEntry, cv2.COLOR_RGB2BGR)
                repEn = getRep(imEntry)
                repEx = getRep(bgrExit)
                if faceMatch(repEn, repEx):
                    #save origFname in personDir
                    print "match found, saving"
                    cv2.imwrite("/Users/riajha/modern-times-server/separated_door1/" + personDir + "/"+ origFName, rgbEntry)
                    imExit = cv2.cvtColor(bgrExit, cv2.COLOR_BGR2RGB)
                    cv2.imwrite("/Users/riajha/modern-times-server/separated_door1/" + personDir + "/"+ fname,imExit)




networkModelPath = "/Users/riajha/openface/models/openface/nn4.small2.v1.t7"
facePredictorPath = "/Users/riajha/openface/models/dlib/shape_predictor_68_face_landmarks.dat"
net = openface.TorchNeuralNet(networkModelPath, 96)

dirName = "/Users/riajha/modern-times-server/door1"
dirA = "/Users/riajha/modern-times-server/facesA"
dirB = "/Users/riajha/modern-times-server/facesB"
dirC = "/Users/riajha/modern-times-server/facesC"
dirD = "/Users/riajha/modern-times-server/facesD"


separate(dirName)