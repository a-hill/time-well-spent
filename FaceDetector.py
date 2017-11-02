from multiprocessing import Process, process
from VideoInterface import VideoInterface
from FaceRecognition import FaceRecognition

class FaceDetector:
    def __init__(self, captureNumber, outputQueue):
        self.outputQueue = outputQueue
        self.process = Process(target=self.run)
        pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
        pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
        self.camera = VideoInterface(captureNumber)
        self.faceRecognition = FaceRecognition(pathToDLibFacePredictor, pathToTorchNeuralNet)
        self.process.start()

    def run(self):
        while True:
            frame, t = self.camera.get_frame_and_time()
            rep = self.faceRecognition.get_rep(frame)
            if rep is not None:
                result = []
                result.append(rep)
                result.append(t)
                self.outputQueue.put(result)


