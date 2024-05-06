import rclpy
from rclpy.node import Node
from niryo_assistant.msg import Locations
from niryo_assistant.msg import CameraDetections

workspace_width = 27.1
workspace_height = 18.5

#robot_zero_to_x = 0.355
#robot_zero_to_y = 0.133

robot_zero_to_x = 0.35
robot_zero_to_y = 0.133

#robot_border_to_x = 0.162
#robot_border_to_y = -0.147

robot_border_to_x = 0.162
robot_border_to_y = -0.158

center_x = 0.256
center_y = -0.0125

zero_id = 0
border_id = 1




def ConvertToWorkspace(point, zero, border):
	height = point[1] - zero[1]
	width = point[0] - zero[0]
	
	height_cm = (height/(border[1] - zero[1])) * workspace_height
	width_cm = (width/(border[0] - zero[0])) * workspace_width
	
	return height_cm, width_cm

class PubSub(Node):
	def __init__(self):
		super().__init__('Localizer')
		self.publisher = self.create_publisher(Locations, "locations_in_workspace", 10)
		self.subscription = self.create_subscription(CameraDetections, 'Detections', self.sub_cb, 10)
		self.subscription
		object_x = []
		object_y = []
		
	def sub_cb(self, msg):
		object_x, object_y = msg.object_x, msg.object_y
		aruco_x, aruco_y = msg.aruco_center_x, msg.aruco_center_y
		aruco_id = msg.aruco_id
		
		cx = []
		cy = []
		
		try:
			zero_x = aruco_x[aruco_id.index(zero_id)]
			zero_y = aruco_y[aruco_id.index(zero_id)]
			
			border_x = aruco_x[aruco_id.index(border_id)]
			border_y = aruco_y[aruco_id.index(border_id)]
			zero = (zero_x, zero_y)
			border = (border_x, border_y)
			
			for idx in range(len(object_x)):
				point = (object_x[idx], object_y[idx])
				point = ConvertToWorkspace(point, zero, border)
				cx.append(robot_zero_to_x - (point[0]/100))
				cy.append(robot_zero_to_y - (point[1]/100))
			self.publish(msg.object_class, msg.object_yaw, cx, cy)
		except Exception as inst:
			print(inst)
	

	def publish(self, object_class, object_yaw, object_x, object_y):
		msg = Locations()
		msg.object_class = object_class
        
		msg.object_yaw = object_yaw
        
		if len(object_x) != 0:
			msg.object_x = object_x
			msg.object_y = object_y
		self.publisher.publish(msg)
		
	
def main():
	rclpy.init(args=None)
	pubsub = PubSub()
	rclpy.spin(pubsub)

if __name__ == '__main__':
	main()
			
		
			
			
			
			
			
			
			
			
		
		
		
	
