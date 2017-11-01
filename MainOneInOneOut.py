from sys import argv
import time
from VideoInterface import VideoInterface
from FaceRecognition import FaceRecognition

class MainOneInOneOut():
	def __init__(self):
	    self.defaultImageDims = 96
	    self.pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
	    self.pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
	    self.faceRecognition = FaceRecognition(self.pathToDLibFacePredictor, self.defaultImageDims, self.pathToTorchNeuralNet)

	def time_difference(self, videoInterface):
	    rep1 = None
	    while rep1 is None:
	    	frame = None
	    	while frame is None:
	        	frame, time1 = videoInterface.get_frame_and_time()
	        rep1 = self.faceRecognition.get_rep(frame, self.defaultImageDims)

	    time.sleep(1)
	    samePerson = False
	    while not samePerson:
	        # obtain and save second face
	        frame2 = None
	        while frame2 is None:
	        	frame2, time2 = videoInterface.get_frame_and_time()
	        rep2 = self.faceRecognition.get_rep(frame2, self.defaultImageDims)
	        samePerson = (self.faceRecognition.is_same_person(rep1, rep2))
	    print(str(time2-time1))

	def run(self):
		inputSource = 0 # If this is an int it refers to a webcam, if string then path to video

		# We have to try casting it to int because if it's a webcam it's an int
		try:
			inputSource = int(argv[1])
		except ValueError:
			inputSource = argv[1]
		except IndexError:
			print "Please give webcam number or path to video as input on command line"
			quit()

		videoInterface = VideoInterface(inputSource)
		
		# Loop forever doing one-in, one-out
		while True:
		    self.time_difference(videoInterface)

main = MainOneInOneOut()
main.run()