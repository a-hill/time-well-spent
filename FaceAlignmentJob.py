from multiprocessing import Process, process
from VideoInterface import VideoInterface
from FaceRecognition import FaceRecognition
import openface
import requests
import cv2

class FaceAlignmentJob:
    BB_SIZE_THRESHOLD = 3500
    FACE_PREDICTOR = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
    URL = 'localhost:5000/submit_face/' #TODO

    def __init__(self, image, time, door, direction):
        self.image     = image
        self.time      = time
        self.door      = door
        self.direction = direction
        self.aligner   = openface.AlignDlib(self.FACE_PREDICTOR)

        process = Process(target=self.run)
        process.start()

    def run(self):
        form = {
            'time'      : str(self.time),
            'door'      : self.door,
        }

        faces = self.align_faces()
        for face in faces:
            files = { 'upload_file' : face }
            requests.post(self.URL + self.direction + '/', files=files, data=form)

    def align_faces(self):
        # Converts image to format expected by aligner
        rgbImg = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        faces = self.aligner.getAllFaceBoundingBoxes(rgbImg)

        alignedFaces = []
        # Crops and rotates each bounding box in the frame
        for face in faces:
            if face.width() * face.height() > self.BB_SIZE_THRESHOLD:
                aligned = self.aligner.align(self.DEFAULT_IMAGE_DIMENSION, rgbImg, face,
                                             landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
                if aligned is not None:
                    alignedFaces.append(aligned)

        return alignedFaces
