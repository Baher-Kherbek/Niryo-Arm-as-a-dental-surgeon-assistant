import cv2
import numpy as np
from math import atan2, cos, sin, sqrt, pi


def drawAxis(img, p_, q_, color, scale):
    p = list(map(int, p_))
    q = list(map(int, q_))

    
    angle = atan2(p[1] - q[1], p[0] - q[0])
    hypotenuse = sqrt((p[1] - q[1]) ** 2 + (p[0] - q[0]) ** 2)

    
    q[0] = p[0] - int(scale * hypotenuse * cos(angle))
    q[1] = p[1] - int(scale * hypotenuse * sin(angle))

    
    cv2.line(img, tuple(p), tuple(q), color, 3)

    
    p[0] = q[0] + int(9 * cos(angle + pi / 4))
    p[1] = q[1] + int(9 * sin(angle + pi / 4))
    cv2.line(img, tuple(p), tuple(q), color, 3)

    p[0] = q[0] + int(9 * cos(angle - pi / 4))
    p[1] = q[1] + int(9 * sin(angle - pi / 4))
    cv2.line(img, tuple(p), tuple(q), color, 3)


def getOrientation(mask, img, draw_axis=True, draw_center=True):
    
    mask = mask.astype(np.uint8)
    img = img.astype(np.uint8)
    masked_frame = cv2.bitwise_and(img, img, mask=mask)
     
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None, None

    max_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(max_contour)
    if M["m00"] == 0:
        return None, None, None
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    max_contour_points = max_contour.reshape(-1, 2).astype(np.float32)  
    pca = cv2.PCACompute2(max_contour_points, mean=None)  
    eigenvectors = pca[1]
    eigenvalues = pca[2]

    if draw_center:
        cv2.circle(masked_frame, center, 10, (0, 0, 255), -1)

    if draw_axis:
        
        p1 = (center[0] + 0.02 * eigenvectors[0, 0] * eigenvalues[0, 0], center[1] + 0.02 * eigenvectors[0, 1] * eigenvalues[0, 0])
        p2 = (center[0] - 0.02 * eigenvectors[1, 0] * eigenvalues[1, 0], center[1] - 0.02 * eigenvectors[1, 1] * eigenvalues[1, 0])
        drawAxis(masked_frame, center, p1, (255, 255, 0), 1)
        #drawAxis(masked_frame, center, p2, (0, 0, 255), 5)

    angle = atan2(eigenvectors[0, 1], eigenvectors[0, 0])
    
    return angle, center, masked_frame

