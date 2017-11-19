from multiprocessing import Process, process
from VideoInterface import VideoInterface
from FaceRecognition import FaceRecognition

class FaceDetector:
    def __init__(self, inputQueue, outputQueue):
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue
        self.process = Process(target=self.run)
        pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
        pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
        self.faceRecognition = FaceRecognition(pathToDLibFacePredictor, pathToTorchNeuralNet)
        self.process.start()

    def run(self):
        while True:
            if not self.inputQueue.empty():
                pair = self.inputQueue.get()
                frame = pair[0]
                t = pair[1]
                reps = self.faceRecognition.get_reps(frame)
                for rep in reps:
                    self.outputQueue.put([rep, t])
