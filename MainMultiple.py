from sys import argv
import time
from VideoInterface import VideoInterface
from FaceRecognition import FaceRecognition

class MainMultiple():
	def __init__(self):
	    self.defaultImageDims = 96
	    self.pathToDLibFacePredictor = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
	    self.pathToTorchNeuralNet = './../openface/models/openface/nn4.small2.v1.t7'
	    self.faceRecognition = FaceRecognition(self.pathToDLibFacePredictor, self.defaultImageDims, self.pathToTorchNeuralNet)
	    self.peopleInRoom = []
	    self.cumulativeTimeSpent = 0

	def detect(self, videoInterface):
	    currentRep = None
	    #Keep searching for a face
	    while currentRep is None:
	    	frame = None
	    	while frame is None:
	        	frame, currentTime = videoInterface.get_frame_and_time()
	        currentRep = self.faceRecognition.get_rep(frame, self.defaultImageDims)

	    #Loop through the list and check if currentRep already exists in the list
	    for rep, entryTime in self.peopleInRoom:
	    	if self.faceRecognition.is_same_person(currentRep, rep):
	    		time_difference = currentTime - entryTime
	    		if time_difference < 3: # This is the case where someone is entering and their face is still in the next frame
	    			print "seen same person again (too soon to be leaving)"
	    		else:
		    		print "seen person leaving"
		    		self.cumulativeTimeSpent = self.cumulativeTimeSpent + time_difference
		    		print "cumulative time spent: " + str(self.cumulativeTimeSpent)
		    		#Remove person from list as they have just left the room
		    		self.peopleInRoom = [p for p in self.peopleInRoom if not self.same(p, (rep, entryTime))]
		    		print str(len(self.peopleInRoom)) + " people are in the room."
		    		print str(time_difference)
		    	return
	    print "seen new person enter"
	    #Add new person to list storing it's vector representation and time
	    self.peopleInRoom.append((currentRep, currentTime))
	    print str(len(self.peopleInRoom)) + " people are in the room."

	def same(self, (a, b), (c, d)):
		if (a == c).all():
			if (b == d):
				return True
		return False

	def run(self):
		inputSource = 0 # If this is an int it refers to a webcam, if string then path to video

		# We have to try casting it to int because if it's a webcam it's an int
		try:
			inputSource = int(argv[1])
		except ValueError:
			inputSource = argv[1]
		except IndexError:
			print "Please give webcam number or path to video as input on command line"
			#Quit program if correct input not given
			quit()

		videoInterface = VideoInterface(inputSource)
		
		# Loop forever, tracking entry and exit of multiple people
		while True:
		    self.detect(videoInterface)

main = MainMultiple()
main.run()