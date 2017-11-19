from multiprocessing import Process
import cv2
from VideoInterface import VideoInterface
from FaceRecognition import FaceRecognition
import requests
import json

entry_url = 'modern-times-1.uksouth.cloudapp.azure.com/submit_face/entry/';
exit_url = 'modern-times-1.uksouth.cloudapp.azure.com/submit_face/exit/';

class Camera:
    def __init__(self, videoInterface, exit):
        pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
        pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
        self.faceRecognition = FaceRecognition(pathToDLibFacePredictor, pathToTorchNeuralNet)
        self.videoInterface = videoInterface
        self.exit = exit
        self.process = Process(target=self.run)



    def run(self):
        while True:
            frame, t = self.videoInterface.get_frame_and_time()
            if frame is not None:
                faces = self.faceRecognition.align_faces(frame)
                if len(faces > 0):
                    if not self.exit:
                        for f in faces:
                            #Check correct format of image, encoding as jpg regardless
                            #If response is empty?
                            _, img_encoded = cv2.imencode('.jpg', f)
                            response = requests.post(entry_url, f)
                    else:
                        for f in faces:
                            # Check correct format of image
                            # If response is empty?
                            _, img_encoded = cv2.imencode('.jpg', f)
                            response = requests.post(exit_url, img_encoded)
                            #Get time difference from response and print
                            print json.loads(response.text)






    if __name__ == '__main__':
        from Camera import Camera
        #One exit cam and one entry cam per computer
        entryCam = Camera(VideoInterface(0),False)
        exitCam = Camera(VideoInterface(1), True)
        entryCam.process.start()
        exitCam.process.start()





