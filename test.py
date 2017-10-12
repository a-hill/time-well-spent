import numpy as np
import cv2

video = cv2.VideoCapture("video.mp4");

# Find OpenCV version
#(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

#if int(major_ver)  < 3 :
#    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
#    print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
#else :
fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS) : {0}".format(fps)

waitPerFrameInMillisec = int( 1/fps * 1000/1 )

while(video.isOpened()):
    ret, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.IMREAD_COLOR)

    cv2.imshow('frame',gray)
    cv2.cv.WaitKey( waitPerFrameInMillisec  )

#    if cv2.waitKey(1) & 0xFF == ord('q'):
#       break

video.release
cap.release()
cv2.destroyAllWindows()
