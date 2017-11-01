from multiprocessing import Process
from VideoInterface import VideoInterface
from FaceRecognition import FaceRecognition

class FaceDetector:
	def __init__(self, captureNumber, outputQueue):
		self.camera = VideoInterface(captureNumber)
		self.outputQueue = outputQueue
		self.process = Process(target=self.run)
		self.process.start()

        pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
        pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
        self.faceRecognition = FaceRecognition(pathToDLibFacePredictor, pathToTorchNeuralNet)

	def run(self):
		while True:
			frame, t = self.camera.get_frame_and_time()
			rep = self.faceRecognition.get_rep(frame)
			if rep is not None:
				result = []
				result.append()
				result.append(t)
				outputQueue.put(result)
