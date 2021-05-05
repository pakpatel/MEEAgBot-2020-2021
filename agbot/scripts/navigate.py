#! /usr/bin/env python
import rospy
import time 
from ackermann_msgs.msg import AckermannDrive

ack_publisher = None
max_speed = 12 # m/s
max_steering = 8 # radians

ack_msg = AckermannDrive()


def traverse():
    print "We're moving"
    drive()
    time.sleep(130)
    steer_right()
    time.sleep(30) 
    drive()
    time.sleep(130)
    steer_left()
    time.sleep(30)
    drive()
    time.sleep(130)
    stop()
	
def drive():
    print "drive"
    ack_msg.steering_angle = 0.0
    ack_msg.speed = 9.0
    print(ack_msg)
    ack_publisher.publish(ack_msg)

def steer_right():
    
    ack_msg.steering_angle = -8.0
    ack_msg.speed = 7.0
    ack_publisher.publish(ack_msg)

def steer_left():
    
    ack_msg.steering_angle = 8.0
    ack_msg.speed = 7.0
    ack_publisher.publish(ack_msg) 

def stop():
    
    ack_msg.steering_angle = 0
    ack_msg.speed = 0
    ack_publisher.publish(ack_msg)    

if __name__ == '__main__':
    rospy.init_node('navigate')
    max_speed = rospy.get_param("~max_speed", 12)
    max_steering = rospy.get_param("~max_steering", 8)
    ack_publisher = rospy.Publisher('cmd_vel', AckermannDrive, queue_size=1)
    traverse()  
    
    while not rospy.is_shutdown():
	      
	rospy.spin()

