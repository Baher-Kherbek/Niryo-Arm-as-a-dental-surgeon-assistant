#/usr/bin/env python3

import rclpy
from rclpy.node import Node
from niryo_assistant.msg import Locations
from niryo_assistant.msg import CameraDetections
import sys
import os
from ssh import *
import numpy as np
import interpolation as in3
class subs(Node):
    def __init__(self):
        super().__init__('Grab')
        self.subscription = self.create_subscription(Locations, 'locations_in_workspace', self.sb_cb, 10)

    def sb_cb(self, data):

        tool = float(sys.argv[1])

        if (tool in data.object_class and len(data.object_x) != 0):
            print('tool found')
            index = data.object_class.index(tool)

            x = data.object_x[index]
            y = data.object_y[index]

            yaw = data.object_yaw[index]

            username = 'niryo'
            hostname = 'niryo-desktop.local'
            password = 'robotics'

            client = SSH(username, hostname, password, 'Desktop/master', 'handler.py')
            angle = yaw
            #if angle < 0:
             #   angle += np.pi
            #yaw_ref=0
            #if angle < yaw_ref:
             #   angle += np.pi
            #elif angle > yaw_ref + np.pi:
                #angle -= np.pi

            angle = -yaw
            if (angle + np.pi/2) <= 2.57:
                angle += np.pi/2
            else:
                angle -= np.pi/2

            #angle += np.pi/2
            #y#aw_ref=0.2
            #if angle < yaw_ref - (np.pi / 2):
            #    angle += np.pi
            #elif angle > yaw_ref + (np.pi / 2):
            #    angle -= np.pi


            yaw_data = [1.77, 0.785, -0.585, -1.37]
            x_data = [8, 0, 4, 8] 
            y_data = [-7, 0, 3, 5]
            new_yaw = yaw

            estimated_x, estimated_y = in3.linear_interpolation(yaw_data, x_data, y_data, new_yaw)

            print("Estimated x for yaw", new_yaw, ":", estimated_x)
            print("Estimated y for yaw", new_yaw, ":", estimated_y)


            command = f'pick {x+0/1000} {y+0/1000} 0.123 0 1.5 {angle+0.2}'

            print('sending')
            client.SendCommand(command)
            sys.exit()


def main():
    rclpy.init(args=None)
    sub = subs()
    rclpy.spin(sub)

main()











