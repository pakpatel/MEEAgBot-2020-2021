#! /usr/bin/env python
import rospy
import time 
from ackermann_msgs.msg import AckermannDrive

ack_publisher = None
max_speed = 12 # m/s
max_steering = 8 # radians

ack_msg = AckermannDrive()


def traverse():
    print "drive"
    ack_msg.steering_angle = 0.0
    ack_msg.speed = 9.0
    print(ack_msg)
    ack_publisher.publish(ack_msg)    

if __name__ == '__main__':
    rospy.init_node('navigate')
    ack_publisher = rospy.Publisher('cmd_vel', AckermannDrive, queue_size=1)
    traverse()  
    
    while not rospy.is_shutdown():
	      
	rospy.spin()

