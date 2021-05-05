#!/usr/bin/env python
# license removed for brevity
import rospy
import time
from ackermann_msgs.msg import AckermannDrive

def start():
    ack_msg = AckermannDrive()
    ack_msg.steering_angle = 0.0
    ack_msg.speed = 9.0
    return ack_msg

def drive():
    ack_msg = AckermannDrive()
    ack_msg.steering_angle = 0.0
    ack_msg.speed = 8.5
    return ack_msg

def left():
    ack_msg = AckermannDrive()
    ack_msg.steering_angle = 8.0
    ack_msg.speed = 7.0
    return ack_msg

def right():
    ack_msg = AckermannDrive()
    ack_msg.steering_angle = -8.0
    ack_msg.speed = 7.0
    return ack_msg

def stop():
    ack_msg = AckermannDrive()
    ack_msg.steering_angle = 0.0
    ack_msg.speed = 0.0
    return ack_msg


def traverse():
    pub = rospy.Publisher('agbot/move_cmd', AckermannDrive, queue_size=10)
    rospy.init_node('navigate', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        ack_msg = AckermannDrive()
        rospy.loginfo(ack_msg)
     



#START
        start_msg= start()
        pub.publish(start_msg)
	rospy.loginfo(start_msg)
        rospy.sleep(10)	


#DRIVE
        drive_msg= drive()
        pub.publish(drive_msg)
	rospy.loginfo(drive_msg)
        rospy.sleep(10)
        
#RIGHT
	left_msg= left()
	pub.publish(left_msg)
        rospy.loginfo(left_msg)
        rospy.sleep(30)
        
#DRIVE
	drive_msg= drive()
        pub.publish(drive_msg)
        rospy.loginfo(drive_msg)
        rospy.sleep(15)
#LEFT
	right_msg= right()
	pub.publish(right_msg)
	rospy.loginfo(right_msg)
        rospy.sleep(30)
#DRIVE
	drive_msg= drive()
        pub.publish(drive_msg)
        rospy.loginfo(drive_msg)
	rospy.sleep(5)
#STOP
	stop_msg= stop()
        pub.publish(stop_msg)
	rospy.loginfo(stop_msg)
	rospy.sleep(500)	

if __name__ == '__main__':
    try:
        traverse()
    except rospy.ROSInterruptException:
        pass

