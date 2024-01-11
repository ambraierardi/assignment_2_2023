Assignment 2 - Research Trach 1
================================

This program is a simple 3D simulation of a robot in an planar environment, with some obstacles inside, using ROS (Robot Operating System).   
The goal of this project was to implement an action client for the given action server, which implements the *bug0* algorithm, a service node returning the last target position, and a last node implementing a server retrieving the distance from the current target and the average robot speed.

Installing and running
----------------------

The simulator requires the ROS installation, following the instructions at this link: https://wiki.ros.org/noetic/Installation/Ubuntu, and the terminal emulator *xterm*, running the following command on the shell: `sudo apt-get -y install xterm`, in order to get a dedicated terminal for every printing node.  
At this point, clone the repository by typing `git clone https://github.com/ambraierardi/assignment2_rt1`.  
Now, simply run the following line: `roslaunch assignment_2_2023 assignment1.launch`on the downloaded folder and follow the instructions on the shell.


Flowchart of the project
----------------------
![Flowchart](Flowchart.drawio.png)

Rosgraph of the processes
----------------------
![Rosgraph](rosgraph.png)
