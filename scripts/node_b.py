#! /usr/bin/env python

# import all necessary stuff

import rospy
from assignment_2_2023.srv import Last_target, Last_targetResponse
import sys
import actionlib
import actionlib.msg

# define the callback function for the service
def callback(msg):
    # get the parameters for the desired position, from the parameter server
    global x,y
    x=rospy.get_param('des_pos_x')
    y=rospy.get_param('des_pos_y')
    # this is the response of the service, with the coordinates of the desired position
    return Last_targetResponse(x,y)


def main():
    # initialize the node with the name service_client, which will be found in the launch file
    rospy.init_node('last_target_node')
    # create the service, with the name last_target, the service type Last_target and the name of the callback function
    rospy.Service('last_target', Last_target, callback)
    # spin
    rospy.spin()


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        # if the program is interrupted before completion, print a message
        print("Program interrupted before completion", file=sys.stderr)
