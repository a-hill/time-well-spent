import StringIO
from multiprocessing import Process
import openface
import requests
import cv2
from PIL import Image

class FaceAlignmentJob:
    BB_SIZE_THRESHOLD = 3500
    FACE_PREDICTOR = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
    DEFAULT_IMAGE_DIMENSION = 96

    def __init__(self, frame, time, door, url):
        self.frame     = frame
        self.time      = time
        self.door      = door
        self.aligner   = openface.AlignDlib(self.FACE_PREDICTOR)
        self.url = url
        self.process = Process(target=self.run)


    def run(self):
        form = {
            'time'      : str(int(self.time)),
            'door'      : self.door,
        }

        #ria version
        # if faces, for each face, send to server
        # for f in faces:
        #         # Check correct format of image, encoding as jpg regardless
        #         # todo: If response is empty or error or timeout etc?
        #         _, img_encoded = cv2.imencode('.jpg',  )
        #         response = requests.post(url, img_encoded)
        #         print json.loads(response.text)
        faces = self.align_faces()
        print 'after aligning faces, faces length: ' + str(len(faces))
        for face in faces:
            cv2.imwrite('face.jpg', face)
            im = Image.fromarray(face)
            buf = StringIO.StringIO()
            im.save(buf, "JPEG", quality=10)
            jpegface = buf.getvalue()
            files = { 'upload_file' : jpegface }
            print 'Request: about to send'
            response = requests.post(self.url, files=files, data=form)
            print response.text

    def align_faces(self):
        # Converts image to format expected by aligner
        print 'in align_faces (start)'
        #rgbImg = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        rgbImg = self.frame
        print 'rgbImg made'
        faces = self.aligner.getAllFaceBoundingBoxes(rgbImg)
        print 'got bounded boxes' + str(len(faces))
        alignedFaces = []
        # Crops and rotates each bounding box in the frame
        for face in faces:
            if face.width() * face.height() > self.BB_SIZE_THRESHOLD:
                aligned = self.aligner.align(self.DEFAULT_IMAGE_DIMENSION, rgbImg, face,
                                             landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
                if aligned is not None:
                    alignedFaces.append(aligned)

        return alignedFaces
