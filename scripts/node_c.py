#! /usr/bin/env python

# import all necessary stuff

import rospy
from assignment_2_2023.srv import Last_target, Last_targetResponse
from assignment_2_2023.msg import Custom
from assignment_2_2023.srv import Dist_ave_vel, Dist_ave_velResponse
import sys
import actionlib
import actionlib.msg
import math
from geometry_msgs.msg import Pose, Twist, Point
from nav_msgs.msg import Odometry
import time

d=0.0
global vel_x
global vel_z
global new_msg
# create the two lists for the velocities
vel_x=[]
vel_z=[]

# define the callback function for the subscriber
def callback(msg):
    global vel_x, vel_z, new_msg
    # create a new message of type Custom
    new_msg=Custom()
    # set the parameters of the new message, with the data from the Custom message
    new_msg.x = msg.x
    new_msg.y = msg.y
    new_msg.v_x = msg.v_x
    new_msg.v_z = msg.v_z
    # append the velocities to the lists
    vel_x.append(new_msg.v_x)
    vel_z.append(new_msg.v_z)
    # get the window size from the launch file
    ws=rospy.get_param('window_size')
    # if the window size is reached, remove the oldest velocity
    if len(vel_x)>ws:
        vel_x.pop(0)
        vel_z.pop(0)

# define the callback function for the service
def serv_callback(req):
    global x,y,d,ave_v_x,ave_v_z
    # get the parameters for the desired position, from the parameter server
    x=rospy.get_param('des_pos_x')
    y=rospy.get_param('des_pos_y')
    # calculate the distance from the target
    d=math.sqrt((x-new_msg.x)**2+(y-new_msg.y)**2) 
    # calculate the average velocities
    ave_v_x=sum(vel_x)/len(vel_x) 
    ave_v_z=sum(vel_z)/len(vel_z)
    # print the results
    print("Distance from the target: ",d)
    print("Average linear velocity along x: ", ave_v_x)
    print("Average angular velocity along z: ", ave_v_z)
    # return the response of the service, with the distance and the average velocities
    return Dist_ave_velResponse(d,ave_v_x,ave_v_z)
    
def main():
    # initialize the node with the name service_client, which will be found in the launch file
    rospy.init_node('pos_vel_srv')
    # create the subscriber, to the topic /pos_and_vel, with the message type Custom and the name of the callback function
    rospy.Subscriber("/pos_and_vel", Custom, callback)
    # create the service, with the name  dist_ave_vel, the service type Dist_ave_vel and the name of the callback function
    rospy.Service('dist_ave_vel', Dist_ave_vel, serv_callback)  
    # spin
    rospy.spin()
    


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        # if the program is interrupted before completion, print a message
        print("Program interrupted before completion", file=sys.stderr)

