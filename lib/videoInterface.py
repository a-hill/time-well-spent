import numpy as np 
import cv2
import time

cameraPort = 0
#TODO: Refactor so that cap is passed in as a parameter
def getFrameFromVideo(videoInput):
	cap = cv2.VideoCapture(videoInput)
	if not isinstance(videoInput, str):
		#Allow time for webcam to wake up
		time.sleep(2)
	ret, frame = cap.read()

	if not ret:
		print "Failed to get frame from video input "
		print(videoInput)
	cap.release()
	return frame


def getFrameFromWebcam():
	getFrameFromVideo(cameraPort)

