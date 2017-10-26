import numpy as np 
import cv2
import time

cameraPort = 0

def getFrameFromVideo(videoInput):
	cap = cv2.VideoCapture(videoInput)
	time.sleep(3)
	ret, frame = cap.read()

	if not ret:
		print "Failed to get frame from video input "
		print(videoInput)
	cv2.imshow('frame', frame)
	cv2.waitKey(10000)
	cap.release()
	return frame


def getFrameFromWebcam():
	getFrameFromVideo(cameraPort)

