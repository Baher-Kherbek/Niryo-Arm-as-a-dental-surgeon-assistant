import numpy as np
from utils.detection import *

class Frame(ArucoDetector):
    def ___init__(self):
        self.frame = None
        self.AnnotatedFrame = None
        self.Arucos = None
        self.circles = None

    def process(self, frame):
        #Get Arucos
        self.frame = frame
        corners, ids, _ = self.DetectMarkers(frame)
        self.AnnotatedFrame = self.DrawMarker(frame, corners)
        centers = self.getCenters(corners)
        
        self.Arucos = dict()
        if ids is not None:
            for idx, val in enumerate(ids):
                self.Arucos[val] = centers[idx]

        #Get Circles
        self.circles = []
        gray = np.copy(frame)
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                                    param1 = 50,
                                    param2 = 70,
                                    minRadius = 0,
                                    maxRadius = 0)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                self.AnnotatedFrame = cv2.circle(self.AnnotatedFrame, (i[0], i[1]), i[2], [255,255,0], 2)
            self.circles = circles[0, :]
   

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    frame = Frame()
    while True:
        img = cap.read()[1]
        frame.process(img)
        print(frame.circles)
        cv2.imshow('fr', frame.AnnotatedFrame)
        if cv2.waitKey(1) == 27:
            break


