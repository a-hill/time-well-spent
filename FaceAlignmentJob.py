import StringIO
import requests
import cv2
import time
from PIL import Image

class FaceAlignmentJob:
    OUTER_EYES_AND_NOSE = [36, 45, 33]
    BB_SIZE_THRESHOLD = 3500

    DEFAULT_IMAGE_DIMENSION = 96

    def __init__(self, frame, t, door, url, aligner):
        self.frame   = frame
        self.t       = t
        self.door    = door
        self.aligner = aligner
        self.url     = url

    def run(self):
        start = time.clock()

        form = {
            'time' : str(int(self.t)),
            'door' : self.door,
        }

        faces = self.align_faces()
        print 'after aligning faces, faces length: ' + str(len(faces))
        for face in faces:
            im = Image.fromarray(face)
            buf = StringIO.StringIO()
            im.save(buf, "JPEG", quality=10)
            jpegface = buf.getvalue()
            files = { 'upload_file' : jpegface }
            requests.post(self.url, files=files, data=form)
        
        print 'This face took: ' + str(time.clock() - start) + ' seconds to align.'

    def align_faces(self):
        # Converts image to format expected by aligner
        rgbImg = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        faces = self.aligner.getAllFaceBoundingBoxes(rgbImg)
        alignedFaces = []
        # Crops and rotates each bounding box in the frame
        for face in faces:
            if face.width() * face.height() > self.BB_SIZE_THRESHOLD:
                aligned = self.aligner.align(self.DEFAULT_IMAGE_DIMENSION, rgbImg, face,
                                             landmarkIndices=self.OUTER_EYES_AND_NOSE)
                if aligned is not None:
                    alignedFaces.append(aligned)

        return alignedFaces
