#! /usr/bin/env python

# import all necessary stuff

import rospy
from std_srvs.srv import *
from geometry_msgs.msg import Pose, Twist, Point
from nav_msgs.msg import Odometry
import assignment_2_2023.msg
from assignment_2_2023.msg import Custom, Feet
from assignment_2_2023.srv import Cancel, CancelResponse
import sys
import select
import actionlib
import actionlib.msg
import time

# define the callback function for the subscriber
def callback(msg):
    # create a new message of type Custom
    new_msg=Custom()
    # set the parameters of the new message, with the data from the Odometry message
    new_msg.x = msg.pose.pose.position.x
    new_msg.y = msg.pose.pose.position.y
    new_msg.v_x = msg.twist.twist.linear.x
    new_msg.v_z = msg.twist.twist.angular.z
    # publish the new message on the topic /pos_and_vel
    pub.publish(new_msg)

# function to get the user input, without blocking the program
def get_user_input(timeout):
    # select the input from the user, with a timeout
    i,_,_=select.select([sys.stdin],[],[],timeout)
    # if there is an input, return it   
    if i:
        return sys.stdin.readline().rstrip()
    else:
        return None

def action_client():
    # create the action client, with the name of the action server as the argument
    global act_cl
    act_cl=actionlib.SimpleActionClient('/reaching_goal',assignment_2_2023.msg.PlanningAction)
    # wait for the action server to start
    act_cl.wait_for_server()
    # until the node is stopped, ask the user for a goal
    while not rospy.is_shutdown():   
        print("\nPlease, enter the x and y coordinates of the goal.")
        try:
            x=float(input("x: "))
            y=float(input("y: "))
        # if the input is not a number, print a message and ask for the goal again   
        except ValueError:
            print("Invalid input! Please only enter numbers.")
            continue
        # create the goal message, with the coordinates entered by the user
        goal=assignment_2_2023.msg.PlanningGoal()
        goal.target_pose.pose.position.x=x
        goal.target_pose.pose.position.y=y
        # send the goal to the action server
        act_cl.send_goal(goal)
        # set the parameters for the desired position, in the relative parameters
        rospy.set_param("des_pos_x",x)
        rospy.set_param("des_pos_y",y)
        print("\nThe robot is reaching the goal. If you want to cancel the goal, press 'c': ")
        # while the goal is not reached, ask the user for an input, without blocking the program
        while act_cl.get_state() != actionlib.GoalStatus.SUCCEEDED:
            user_input=get_user_input(1)
            if user_input=='c':
                # if the user presses 'c', cancel the goal and break the loop
                act_cl.cancel_goal()
                rospy.loginfo("Goal cancelled.")
                break
def cb(msg):
	new_msg=Feet()
	a=msg.pose.pose.position.x
	new_msg.x=a*3.28
	b=msg.pose.pose.position.y
	new_msg.y=b*3.28
	pub1.publish(new_msg)

def callb(msg):
	act_cl.cancel_goal()
	return True
        
def main():
    # define the publisher globally, to modify it in the subscriber callback
    global pub, pub1
    # initialize the node with the name that will be found in the launch file
    rospy.init_node("actionclient")
    # create the publisher, which publishes on the topic /pos_and_vel, with a message of type Custom, and queue size=10
    pub = rospy.Publisher("/pos_and_vel", Custom, queue_size=10)
    pub1=rospy.Publisher("/pos_in_feet", Feet, queue_size=10)
    rospy.Subscriber("/odom", Odometry, cb)
    # create the subscriber to the topic /odom, of type Odometry, and the created callback function
    rospy.Subscriber("/odom", Odometry, callback)
    rospy.Service("/cancel_goal", Cancel, callb)
    # until the node is stopped, call the action_client function and spin
    while not rospy.is_shutdown():
        action_client()
        rospy.spin()


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        # if the node is stopped, print a message
        print("program interrupted before completion", file=sys.stderr)
