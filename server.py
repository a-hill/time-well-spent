from flask import Flask, request
import cv2
import re
import numpy as np
from PIL import Image

from FaceRecognition import FaceRecognition
app = Flask(__name__)

facePredictorPath = './../openface/models/dlib/shape_predictor_68_face_landmarks.dat'
networkModelPath = './../openface/models/openface/nn4.small2.v1.t7'
        

faceRecognition = FaceRecognition(facePredictorPath, networkModelPath)

def valid_filename(filename):
	pattern = re.compile('[0-9]+\.jpe?g')
	return re.search(pattern, filename) is not None
	
def process_image(request):
	#check that user submitted a file
	if 'fileToUpload' not in request.files:
		print 'client did not submit a file. ignoring.'
		return None
	
	#get file
	file = request.files['fileToUpload'] # may also be request.files['file']
	
	#check validity of filename
	if not valid_filename(file.filename):
		print 'client submitted a file with an invalid filename'
		return None
		
	#read file from stream into array
	image = file.stream.read()
	string = np.fromstring(image, dtype='uint8')
	data = cv2.imdecode(string, cv2.IMREAD_COLOR)

	#get rep
	rep = faceRecognition.get_rep_from_aligned(data)
	
	return rep
		

@app.route("/submit_face/entry/", methods=['POST'])
def face_enter():
	successResponse = 'success'
	failResponse = 'fail'
	
	rep = process_image(request)
	if rep is None:
		return failResponse
	else:
		print 'success:', rep
				
	return successResponse
	
@app.route("/submit_face/exit/", methods=['POST'])
def face_exit():
	successResponse = 'success'
	failResponse = 'fail'
	
				
	return successResponse	
	
@app.route("/cumulative_time/", methods=['GET'])
def get_time():
	#TODO
	return 0
	
if __name__ == "__main__":
	app.run()