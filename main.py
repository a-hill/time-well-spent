from multiprocessing import Process
from FaceRecognition import FaceRecognition
from VideoInterface import VideoInterface
import cv2
import sys
import requests
import json
import time


class Main:
    def __init__(self, videoInterface, exit, url):
        self.url = url
        self.MAX_FRAMERATE = 0.2  # five frames per second
        pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
        pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
        self.faceRecognition = FaceRecognition(pathToDLibFacePredictor, pathToTorchNeuralNet)
        self.videoInterface = videoInterface
        self.exit = exit
        self.process = Process(target=self.run)

    def run(self):
        while True:
            # start rate limiting
            start = time.clock()

            # take frame and get time
            frame, t = self.videoInterface.get_frame_and_time()

            # todo: if frame is none????
            if frame is not None:
                faces = self.faceRecognition.align_faces(frame)

                # if faces, for each face, send to server
                if len(faces > 0):
                    for f in faces:
                        # Check correct format of image, encoding as jpg regardless
                        # todo: If response is empty or error or timeout etc?
                        _, img_encoded = cv2.imencode('.jpg', f)
                        response = requests.post(url, img_encoded)
                        print json.loads(response.text)

            # rate limiting
            delta = (time.clock() - start) * 1000
            if delta < self.MAX_FRAMERATE:
                time.sleep(self.MAX_FRAMERATE - delta)


# Arguments - main.py cameraNum exit/entry
if __name__ == '__main__':

    entry_url = 'modern-times-1.uksouth.cloudapp.azure.com/submit_face/entry/'
    exit_url = 'modern-times-1.uksouth.cloudapp.azure.com/submit_face/exit/'

    camera_id = int(sys.argv[1])

    if sys.argv[2] is 'exit':
        is_exit = True
    else:
        is_exit = False

    url = exit_url if is_exit else entry_url
    # One exit cam and one entry cam per computer
    main = Main(VideoInterface(camera_id), is_exit, url)
    # todo creates new process - needed???
    main.process.start()
