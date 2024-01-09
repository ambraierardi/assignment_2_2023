#! /usr/bin/env python

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


global vel_x=[]
global vel_z=[]
window_size=10 #poi modifica perché va introdotta nel launch file!!!!

def callback(msg):
    global new_msg
    new_msg=Custom()
    new_msg.x = msg.pose.pose.position.x
    new_msg.y = msg.pose.pose.position.y
    new_msg.v_x = msg.twist.twist.linear.x
    new_msg.v_z = msg.twist.twist.angular.z
    vel_x.append(new_msg.v_x)
    vel_z.append(new_msg.v_z)
    if len(vel_x)>window_size:
        vel_x.pop(0)
        vel_z.pop(0)
    
def serv_callback(req):
    global x,y
    x=rospy.get_param('des_pos_x')
    y=rospy.get_param('des_pos_y')
    dist=math.sqrt((x-new_msg.x)**2+(y-new_msg.y)**2) #nel .srv si chiama d e non dist
    ave_vel_x=sum(vel_x)/len(vel_x) #nel .srv si chiama ave_v_x e non ave_vel_x
    ave_vel_z=sum(vel_z)/len(vel_z) #nel .srv si chiama ave_v_z e non ave_vel_z
    return Dist_ave_velResponse(dist,ave_vel_x,ave_vel_z)


def main():
    rospy.init_node('pos_vel_srv')
    rospy.Subscriber('/pos_and_vel', Custom, callback)
    rospy.Service('dist_ave_vel', Dist_ave_vel, serv_callback)

    rospy.spin()


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        print("Program interrupted before completion", file=sys.stderr)
