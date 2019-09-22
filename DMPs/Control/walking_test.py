# test the dmp
import sys
sys.path.append('/home/student/Documents/DM/DMPs/Control')
sys.path.append('/home/student/Documents/DM/DMPs/Control/Controllers')



import Controllers.dmp as dmp  # import the dmp for controller
#import Tasks.walk as walk # import the walking data for trajectory
#import Tasks.knee as walk # import the walking data for trajectory
from Tasks.Knee import knee

import numpy as np
#import matplotlib.pyplot as plt
import pdb

import pydmps.dmp_rhythmic
alpha = 75. #by default
beta = alpha / 4 # by default
#beta = 20.0 / np.pi
#gamma = 100

def interaction_force():
# this gives the interaction force for the system
# exo torque or force
	force_points = 25 #numero de point pour interaction
	int_force = np.random.random((force_points, 1))*20 #limite des force max 20N # check if one or points
	return int_force

#test to see if the things work
#if __name__ == "__main__":
# lire les files des trajectories knee data
# call rhythmic dynamic
# 2nd.. 3rd trajectories bata C values learn

# in case of exo.. torque.. impedance control.. learning
dt = 1e-3
random_force_data = interaction_force()


control_shell1, runner_pars1 = knee(file_name1 = "./Tasks/Walk/working_data_2_3/myFile.csv", file_name2 = "./Tasks/Walk/working_data_2_3/minimum_points.csv")
#control_shell1, runner_pars1 = knee(file_name1 = "./Tasks/Walk/force/myfile.csv", file_name2 = "./Tasks/Walk/force/indx.csv")

#control_shell2, runner_pars2 = knee(file_name = ["walking_test2.csv"])
#for each consecutive step
#modulate dmp to change phi..
#get coupling term from dmp1 and pass to dmp2
#get coupling term from dmp2 and pass to next step of dmp 1
#update step values
# ILC for next trajectory
