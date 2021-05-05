#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32 
from std_msgs.msg import Int32
from geometry_msgs.msg import TwistStamped 
from ackermann_msgs.msg import AckermannDriveStamped
from ackermann_msgs.msg import AckermannDrive
from math import pow, atan2, sqrt, sin, cos, radians
import numpy as np


global speed_error
global desired_speed
global speedometer
global speed_to_vehicle
speed_error = 0.0
desired_speed = 0.0
speedometer = 0.0
speed_to_vehicle = 0.0
i_count = 0




def msg_callback(mb_speed):

    '''
    Scale move_base and teleop velocity command to min and max ESC motor control.

    '''
    global desired_speed
    desired_speed = mb_speed.drive.speed

    ackermann_msg = AckermannDrive()
    ackermann_msg.steering_angle = mb_speed.drive.steering_angle
    ackermann_msg.speed = speed_to_vehicle
    print(speed_to_vehicle)
    pub_move.publish(ackermann_msg) 



# ExpMoving Average to smooth out instant speed
instant_speed_history = []
exp_speed_history = []
current_exp_speed = 0.0

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def speed_callback(vel_msg):
    global speedometer
    global VELOCITY_Ki
    global I_COUNT_SETPOINT
    global speed_error
    global i_count
  
    if (np.isnan(vel_msg.twist.linear.x) or np.isnan(vel_msg.twist.linear.y)):
        vel_x = 0
        vel_y = 0
    else:
        vel_x = vel_msg.twist.linear.x
        vel_y = vel_msg.twist.linear.y

    speedometer = sqrt(vel_x**2 + vel_y**2)
    
    # Filter speed estimate
    global exp_speed_history
    global current_exp_speed
    global speed_to_vehicle

    instant_speed_history.append(speedometer)

    if (len(instant_speed_history) > 20):
        exp_speed_history = ExpMovingAverage(instant_speed_history, 5)
        current_exp_speed = float(exp_speed_history[-1])
        instant_speed_history.pop(0)
        exp_speed_history = np.delete(exp_speed_history, 1)

    
    # Use I to control speed
    current_speed_error = desired_speed - current_exp_speed
    speed_correction = speed_error * VELOCITY_Ki
    speed_to_vehicle = desired_speed + speed_correction + current_speed_error
    
    if i_count > I_COUNT_SETPOINT:
        i_count = 0
        speed_error = 0
    else:
        i_count = i_count + 1
        speed_error = speed_error + current_speed_error

    pub_speed.publish(float(speedometer))
    pub_exp_speed.publish(current_exp_speed)


if __name__ == '__main__':
    try:
        rospy.init_node('agbot_base_controller')

        VELOCITY_Ki = float(rospy.get_param('~velocity_ki', '.15'))
        I_COUNT_SETPOINT = float(rospy.get_param('~i_count_setpoint', '15'))

        rospy.Subscriber('/ackermann_cmd', AckermannDriveStamped, msg_callback, queue_size=10)
        rospy.Subscriber('/tcpvel', TwistStamped, speed_callback, queue_size=10)

        pub_speed = rospy.Publisher('/agbot/instant_speed', Float32, queue_size=10)
        pub_exp_speed = rospy.Publisher('/agbot/exp_instant_speed', Float32, queue_size=10)

        pub_move = rospy.Publisher('/agbot/move_cmd', AckermannDrive, queue_size=10) 

        # rospy.loginfo("Node started. \nListening to 'Steer_max',  param value:  %s " % STEERING_MAX ) 
        
	rate = rospy.Rate(30)
 	while not rospy.is_shutdown():
		rate.sleep()

    except rospy.ROSInterruptException:
        pass
