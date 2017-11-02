from multiprocessing import Queue
from FaceDetector import FaceDetector
from FaceRecognition import FaceRecognition
import time


class Main():
    def __init__(self):

        self.entryQueue = Queue()
        self.exitQueue = Queue()
        self.faceDetectors = []
        self.facesInRoom = []

        cameras = [
            [0, "entry"],
            [1, "exit"]
        ]

        for camera in cameras:
            if camera[1] == "entry":
                #Set up an entrance camera
                self.faceDetectors.append(FaceDetector(camera[0], self.entryQueue))
            else:
                #Set up an exit camera
                self.faceDetectors.append(FaceDetector(camera[0], self.exitQueue))

    def run(self):
        while True:
            # check for people entering
            if not self.entryQueue.empty():
                #Get an element from the output queue and check if this person already exists in the list
                elem = self.entryQueue.get()
                if not any(FaceRecognition.is_same_person(x[0], elem[0]) for x in self.facesInRoom):
                    #Adding any new people ie. those that aren't found in the list
                    self.facesInRoom.append(elem)

            # check for people exiting
            if not self.exitQueue.empty():
                elem = self.exitQueue.get()
                newFacesInRoom = []
                for face in self.facesInRoom:
                    if FaceRecognition.is_same_person(face[0], elem[0]):
                        print("This person was in the room for: ", time.time() - face[1], " seconds")
                    else:
                        newFacesInRoom.append(face)

                self.facesInRoom = newFacesInRoom


main = Main()
main.run()