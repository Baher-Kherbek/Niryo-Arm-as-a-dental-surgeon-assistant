import rclpy
from rclpy.node import Node
from niryo_assistant.msg import CameraDetections
from frame import *
from detection import *
import sys
import cv2

cap = cv2.VideoCapture(int(sys.argv[1]))
frame = Frame()
mtx = np.array([[685.74, 0, 311.84], [0, 676.15, 231.55], [0, 0, 1]])
d_c = np.array([-4.3e-01, 4e-01, -5.62e-04, 1.542e-03, -6.56e-01])


class Publisher(Node):
	def __init__(self):
		super().__init__('Camera')
		self.publisher = self.create_publisher(CameraDetections, "Detections", 10)
		timer_period = 0.5
		#self.timer = self.create_timer(timer_period, self.tcallback)
		
		
		#Load Model
		weights = '/home/ayoosh/Desktop/www/best.pt'
		print('Loading Weights')
		self.detector = ObjectsDetector(weights)
		print('weights loaded')
		self.aruco_id = []
		self.aruco_center_x = []
		self.aruco_center_y = []
		self.object_class = []
		self.object_x = []
		self.object_y = []
		self.Con()
	
	def tcallback(self):
		
		#print(self.aruco_center_x)
		#print(self.aruco_center_y)
		msg = CameraDetections()
		msg.object_class = self.object_class
		msg.object_x = self.object_x
		msg.object_y = self.object_y
		msg.aruco_id = list(self.aruco_id)
		msg.aruco_center_x = self.aruco_center_x
		msg.aruco_center_y = self.aruco_center_y
		self.publisher.publish(msg)
	
	def HandleAruco(self, Arucos):
		self.aruco_id = []
		self.aruco_center_x = []
		self.aruco_center_y = []
		
		if Arucos != {}:
			self.aruco_id = list(Arucos.keys())
			for i in range(len(self.aruco_id)):
				self.aruco_id[i] = int(self.aruco_id[i])
			self.aruco_center_x, self.aruco_center_y = list(zip(*list(Arucos.values())))
	
	def HandleObjects(self, detected):
		self.object_x = []
		self.object_y = []
		self.object_class = list(detected[0])
		
		for i in range(len(self.object_class)):
			self.object_class[i] = float(self.object_class[i])
			
		
		for xyxy in detected[1]:
			top = (int(xyxy[0]), int(xyxy[1]))
			bottom = (int(xyxy[2]), int(xyxy[3]))
			Cx = (top[0] + bottom[0]) // 2
			Cy = (top[1] + bottom[1]) // 2
			
			self.object_x.append(Cx)
			self.object_y.append(Cy)
		print(f'CLASS: {self.object_class}')
		print(f'CX : {self.object_x}')
		print(f'CY : {self.object_y}')
        	
        		
		
	def Con(self):
		while True:
			img = cap.read()[1]
			img = cv2.undistort(img, mtx, d_c)
			frame.process(img, getCircles=False)
			self.HandleAruco(frame.Arucos)
			self.detector.DetectObjects(img)
			self.HandleObjects(self.detector.detected_objects)
			self.tcallback()
			cv2.imshow('fr', self.detector.AnnotatedFrame)
			if cv2.waitKey(1) == 27:
				break


def main():
	rclpy.init(args=None)
	pub = Publisher()
	rclpy.spin(pub)
	


if __name__ == '__main__':
	main()
