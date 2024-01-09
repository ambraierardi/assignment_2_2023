#! /usr/bin/env python
import rospy
from std_srvs.srv import *
from geometry_msgs.msg import Pose, Twist, Point
from nav_msgs.msg import Odometry
import assignment_2_2023.msg
from assignment_2_2023.msg import Custom
import sys
import select
import actionlib
import actionlib.msg

def callback(msg):
    global pub
    new_msg=Custom()
    new_msg.x = msg.pose.pose.position.x
    new_msg.y = msg.pose.pose.position.y
    new_msg.v_x = msg.twist.twist.linear.x
    new_msg.v_z = msg.twist.twist.angular.z
    pub.publish(new_msg)

def get_user_input(timeout):
    i,_,_=select.select([sys.stdin],[],[],timeout)
    if i:
        return sys.stdin.readline().rstrip()
    else:
        return None

def action_client():
    act_cl=actionlib.SimpleActionClient('/reaching_goal',assignment_2_2023.msg.PlanningAction)
    act_cl.wait_for_server()
    while not rospy.is_shutdown():
        print("\nEnter the x and y coordinates of the goal")
        try:
            x=float(input("x: "))
            y=float(input("y: "))
        except ValueError:
            print("Invalid input")
            continue
        goal=assignment_2_2023.msg.PlanningGoal()
        goal.target_pose.pose.position.x=x
        goal.target_pose.pose.position.y=y
        act_cl.send_goal(goal)
        rospy.set_param("des_pos_x",x)
        rospy.set_param("des_pos_y",y)
        #prova:
        desx=rospy.get_param("des_pos_x")
        desy=rospy.get_param("des_pos_y")
        rospy.loginfo(desx)
        rospy.loginfo(desy)
        #fine prova


        print("\nIf you want to cancel the goal, press 'c': ")
        feedback=assignment_2_2023.msg.PlanningFeedback()   
        while feedback.stat!="Target reached!":
            user_input=get_user_input(1)
            if user_input=='c':
                act_cl.cancel_goal()
                rospy.loginfo("Goal cancelled")
                break
        
def main():
    global pub
    rospy.init_node("actionclient")
    pub = rospy.Publisher("/pos_and_vel", Custom, queue_size=10)
    rospy.Subscriber("/odom", Odometry, callback)
    action_client()
    rospy.spin()


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)
