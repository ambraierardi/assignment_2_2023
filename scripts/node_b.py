#! /usr/bin/env python

# import all necessary stuff

import rospy
from assignment_2_2023.srv import Last_target, Last_targetResponse
import sys
import actionlib
import actionlib.msg

def callback(msg):
    global x,y
    x=rospy.get_param('des_pos_x')
    y=rospy.get_param('des_pos_y')
    return Last_targetResponse(x,y)


def main():
    rospy.init_node('last_target_node')
    
    rospy.Service('last_target', Last_target, callback)
    
    rospy.spin()


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        print("Program interrupted before completion", file=sys.stderr)
