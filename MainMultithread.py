from multiprocessing import Queue
from FaceDetector import FaceDetector
from FaceRecognition import FaceRecognition
import time


class Main():
    def __init__(self):
        self.entry = Queue()
        self.exit = Queue()
        self.faceDetectors = []
        self.facesInRoom = []

        cameras = [
            [0, "entry"],
            [1, "exit"]
        ]

        for camera in cameras:
            if camera[1] == "entry":
                self.faceDetectors.append(FaceDetector(camera[0], self.entry))
            else:
                self.faceDetectors.append(FaceDetector(camera[0], self.exit))

    def run(self):
        while True:
            # check for people entering
            if not self.entry.empty():
                elem = self.entry.get()
                if not any(FaceRecognition.is_same_person(x[0], elem[0]) for x in self.facesInRoom):
                    self.facesInRoom.append(elem)

            # check for people exiting
            if not self.exit.empty():
                elem = self.entry.get()
                newFacesInRoom = []
                for face in self.facesInRoom:
                    if FaceRecognition.is_same_person(face[0], elem[0]):
                        print("This person was in the room for: ", time.time() - face[1], " seconds")
                    else:
                        newFacesInRoom.append(face)

                self.facesInRoom = newFacesInRoom


