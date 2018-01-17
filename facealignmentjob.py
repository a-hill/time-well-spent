import StringIO
import requests
import cv2
from PIL import Image
from termcolor import colored


class FaceAlignmentJob:
    """Runnable, ran per frame, calls align_face
    on all faces in the frame and posts them to the server"""

    _OUTER_EYES_AND_NOSE = [36, 45, 33]
    _BB_SIZE_THRESHOLD = 4000

    _DEFAULT_IMAGE_DIMENSION = 96
    _TIMEOUT = 1.0  # in seconds

    def __init__(self, frame, t, door, url, aligner):
        self.frame = frame
        self.t = t
        self.door = door
        self.aligner = aligner
        self.url = url

    def run(self):
        form = {
            'time': str(int(self.t)),
            'door': self.door,
        }

        direction = 'entry' if 'entry' in self.url else 'exit'

        faces = self.align_faces()
        # print 'after aligning faces, faces length: ' + str(len(faces))

        if len(faces) > 0:
            print colored('frame on ' + direction + ': ' + str(len(faces)),
                          'green')
        else:
            print 'frame empty ' + direction

        i = 0
        for face in faces:
            i = i + 1
            im = Image.fromarray(face)
            buf = StringIO.StringIO()
            im.save(buf, "JPEG", quality=10)
            jpeg_face = buf.getvalue()
            files = {'upload_file': jpeg_face}

            try:
                requests.post(self.url, files=files,
                              data=form, timeout=self.TIMEOUT)
            except:
                print colored('client on door: ' + str(self.door) +
                              ' failed to connect to server, not sending ' +
                              'aligned face', 'red')

            # direction = 'entry' if 'entry' in self.url else 'exit'
            filename = './faces/' + form['time'] + '-' + \
                       direction + '-' + str(i) + '.jpg'

            cv2.imwrite(filename, face)

    def align_faces(self):
        # Converts image to format expected by aligner
        rgb_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        faces = self.aligner.getAllFaceBoundingBoxes(rgb_img)
        aligned_faces = []
        # Crops and rotates each bounding box in the frame
        for face in faces:
            if face.width() * face.height() > self._BB_SIZE_THRESHOLD:
                aligned = self.aligner.align(
                    self._DEFAULT_IMAGE_DIMENSION, rgb_img, face,
                    landmarkIndices=self._OUTER_EYES_AND_NOSE)
                if aligned is not None:
                    aligned_faces.append(aligned)

        return aligned_faces
