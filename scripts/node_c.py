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


global vel_x
global vel_z
global new_msg
vel_x=[]
vel_z=[]

window_size=10 #poi modifica perché va introdotta nel launch file!!!!

def callback(msg):
    global vel_x, vel_z, new_msg
    new_msg=Custom()
    new_msg.x = msg.x
    new_msg.y = msg.y
    new_msg.v_x = msg.v_x
    new_msg.v_z = msg.v_z
    vel_x.append(new_msg.v_x)
    vel_z.append(new_msg.v_z)
    if len(vel_x)>window_size:
        vel_x.pop(0)
        vel_z.pop(0)


def serv_callback(req):
    global x,y,d,ave_v_x,ave_v_z
    x=rospy.get_param('des_pos_x')
    y=rospy.get_param('des_pos_y')
    d=math.sqrt((x-new_msg.x)**2+(y-new_msg.y)**2) 
    ave_v_x=sum(vel_x)/len(vel_x) 
    ave_v_z=sum(vel_z)/len(vel_z) 
    print("Distance from the goal: ")
    print("Average linear velocity along x: ", ave_v_x)
    print("Average angular velocity along z: ", ave_v_z)
    return Dist_ave_velResponse(d,ave_v_x,ave_v_z)
    
def main():

    
    rospy.init_node('pos_vel_srv')
    
    rospy.Subscriber("/pos_and_vel", Custom, callback)
    
    rospy.Service('dist_ave_vel', Dist_ave_vel, serv_callback)

    rospy.spin()
    


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        print("Program interrupted before completion", file=sys.stderr)
  
        
        
        
      
      
      
      
      
      
      
