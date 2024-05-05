# Niryo-Arm-as-a-dental-surgeon-assistant 

<h2> The Goal </h2>
The goal of the project is to convert the Niryo one robot arm to be used an assitant that handles surgical tools and hands it to the surgeon upon his request


<h2> Methods Used </h2>
A Machine learning model was trained based on the <super>YOLOv8 Segmentation</super> and classification algorithm, the model was trained on a dataset that we created, which consists of images and augmentations of 10 classes of tools. Preforming the Principal Component Anlysis(PCA) algorithm on the contour of the segmented image yields the orientation of the desired tool which will be used to compute the yaw angle of the gripper. Also using the segmented image, we compute the center of gravity of the tool to extract the x and y coordinates for which the arm to grab. As for the Z coordinate, it is set as a constant 0.125m above the table.
The entire project is done in the ROS environment using ROS2 humble on ubuntu 22.04.

<h2> rqt_graph </h2>

![rqt](https://github.com/Baher-Kherbek/Niryo-Arm-as-a-dental-surgeon-assistant/assets/103322810/868a8f86-2c41-4b0b-a4b6-6fde3c68bf61)

<h2> Acknowledgements </h2>
This project is a graduation project for my bachelor's degree in Mechatronics at Tishreen University.
Special acknowledgement to the supervisor of the project, Dr. Nael Daoud


