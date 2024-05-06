#! /usr/bin/env python

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import numpy as np
from torch import device
import cv2
import cv2.aruco

class ObjectsDetector():
    def __init__(self, weights):
        self.model = YOLO(weights).to('cuda')
        self.device = device('cuda:0')
        self.detection_result = None
        self.detected_objects = []
        self.masks = None
        self.frame = None
        self.AnnotatedFrame = None

    def DetectObjects(self, frame):
        self.result = self.model.predict(frame, device=self.device)[0]
        self.detected_objects.append(self.result.names)
        self.detected_objects.append(self.result.cpu().boxes.cls.numpy())
        self.detected_objects.append(self.result.boxes.xyxy.cpu().numpy())
        self.masks = self.result.masks

        self.AnnotatedFrame = self.AnnotateFrame(frame)

    def AnnotateFrame(self, frame):
        xyxy = self.result.boxes.xyxy
        classes = self.result.cpu().boxes.cls.numpy()
        annotator = Annotator(frame)

        for i in range(len(xyxy.cpu().numpy())):
            annotator.box_label(xyxy[i], self.model.names[int(classes[i])], color=[0,0,255])

        return annotator.result()

class ArucoDetector():
    def __init__(self):
        ArucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        ArucoParameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(ArucoDict, ArucoParameters)
        self.corners =[]
        self.ids = None
        self.centers = []
        self.found = False

    def DetectMarkers(self, frame):
        corners, ids, rej = self.detector.detectMarkers(frame)
        if ids is not None:
            ids = ids.flatten()
            self.found = True
        else:
            self.found = False

        return corners, ids, rej

    def DrawMarker(self, frame, corners):
        frame = cv2.aruco.drawDetectedMarkers(frame, corners)
        #self.centers = self.getCenters(self.corners)
        #frame = self.drawPoints(frame, self.centers)
        return frame

    def drawPoints(self, frame, points, color=[255,0,255], radius=5, fill=-1):

        for point in points:
            frame = cv2.circle(frame, point, radius, color, fill)
        return frame

    def getCenters(self, arucos):
        centers = []
        x = 0
        y = 0

        for aruco in arucos:
            for corner in aruco[0]:
                x += corner[0]
                y += corner[1]

            centers.append((int(x//4), int(y//4)))
            x = 0
            y = 0

        return centers




