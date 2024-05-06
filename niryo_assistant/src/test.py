import cv2
import sys
import numpy as np
cap = cv2.VideoCapture(int(sys.argv[1]))
mtx = np.array([[685.74, 0, 311.84], [0, 676.15, 231.55], [0, 0, 1]])
d_c = np.array([-4.3e-01, 4e-01, -5.62e-04, 1.542e-03, -6.56e-01])


while True:
	frame = cap.read()[1]
	frame = cv2.undistort(frame, mtx, d_c)
	
	cv2.imshow('fr', frame)
	if cv2.waitKey(1) == 27:
		break
