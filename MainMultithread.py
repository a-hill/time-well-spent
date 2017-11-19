from multiprocessing.queues import SimpleQueue
from FaceDetector import FaceDetector
from FaceRecognition import FaceRecognition
from VideoInterface import VideoInterface
import time
import random


class Main():
    def __init__(self):
        random.seed()
        self.entryFrameQueue = SimpleQueue()
        self.exitFrameQueue = SimpleQueue()
        self.entryRepQueue = SimpleQueue()
        self.exitRepQueue = SimpleQueue()

        self.faceDetectors = []
        self.facesInRoom = []

        self.cameras = [
            [VideoInterface(0), "entry"],
            [VideoInterface(1), "exit"]
        ]

        # create detectors for entrance camera(s)
        self.faceDetectors.append(FaceDetector(self.entryFrameQueue, self.entryRepQueue))

        # create detectors for exit camera(s)
        self.faceDetectors.append(FaceDetector(self.exitFrameQueue, self.exitRepQueue))


    def run(self):
        while True:
            # get frame from one camera only for load balancing reasons
            for camera in self.cameras:
                frame, t = camera[0].get_frame_and_time()
                if camera[1] == "entry":
                    self.entryFrameQueue.put([frame, t])
                else:
                    self.exitFrameQueue.put([frame, t])

            # compare representations of entering faces
            while not self.entryRepQueue.empty():
                print("face found on entry camera")
                elem = self.entryRepQueue.get()
                # This is a face coming into the room that needs to be added
                if not any(FaceRecognition.is_same_person(x[0], elem[0]) for x in self.facesInRoom):
                    print("new face added to room")
                    # Adding any new people ie. those that aren't found in the list
                    self.facesInRoom.append(elem)

            # compare representations of leaving faces
            while not self.exitRepQueue.empty():
                print("face found on exit camera")
                #This is a face leaving the room that needs to be removed
                elem = self.exitRepQueue.get()
                newFacesInRoom = []
                for face in self.facesInRoom:
                    if FaceRecognition.is_same_person(face[0], elem[0]):
                        print("This person was in the room for: ", elem[1] - face[1], " seconds")
                    else:
                        newFacesInRoom.append(face)

                self.facesInRoom = newFacesInRoom

            print(str(len(self.facesInRoom)) + " faces currently in the room.")


main = Main()
main.run()