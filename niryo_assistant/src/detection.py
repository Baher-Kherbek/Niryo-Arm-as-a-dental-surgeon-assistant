#! /usr/bin/env python

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import numpy as np
from torch import device
import cv2
import cv2.aruco

class ObjectsDetector():
    def __init__(self, weights):
        self.model = YOLO(weights)
        self.detection_result = None
        self.detected_objects = []
        self.device='cpu'
        self.masks = None
        self.frame = None
        self.AnnotatedFrame = None

    def DetectObjects(self, frame):
        self.result = self.model.predict(frame, device=self.device, conf=0.4)[0]
        #self.detected_objects.append(self.result.names)
        self.detected_objects = []
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

        return corners, ids




