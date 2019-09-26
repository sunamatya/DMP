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
alpha = 8 #by default
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
#file_name1 = 'all_data/myfile4.csv'
#file_name2 = 'all_data/indxR4.csv'


#control_shell1, runner_pars1 = knee(file_name1 = "./Tasks/all_data/myfile4.csv", file_name2 = "./Tasks/all_data/indxR4.csv")

y_target_left = np.zeros((0))
y_target_right = np.zeros((0))
y_tracked_left = np.zeros((0))
y_tracked_right = np.zeros((0))
Q = 0
L = 0
c = 0.5


c_range = np.arange(0.1, 0.9, 0.1)
Q_range = np.arange(0.1, 1, 0.1)
L_range = np.arange(0.1, 0.5, 0.1)
minC = 0
minQ = 0
min_rmse = 1000
mocktime = 0

for i in range (c_range.shape[0]):
	#for j in range (Q_range.shape[0]):
		#for k in range (L_range.shape[0]):
		#file_name1 = "./Tasks/Walk/working_data_2_3/myFile.csv"
		#file_name2 = "./Tasks/Walk/working_data_2_3/minimum_points.csv"
		#file_name1 = "./Tasks/all_data/myfile4.csv"
		#file_name2 = "./Tasks/all_data/indxR4.csv"
		# file_name1 = "./Tasks/fwddata/myfile_TS1.csv"
		# file_name2 = "./Tasks/fwddata/indx_TS1_L.csv"
		
	file_name1 = "./Tasks/fwddata/myfile_TS5.csv"
	file_name2 = "./Tasks/fwddata/indx_TS5_L.csv"
	c = c_range[i]
	#Q = Q_range[j]
	#L = L_range[k]
	y_target_left_1, y_target_right_1, y_tracked_left_1,y_tracked_right_1,time = knee(file_name1, file_name2, Q, L, c)
	y_target_left = np.concatenate((y_target_left, y_target_left_1))
	y_target_right = np.concatenate((y_target_right, y_target_right_1))
	y_tracked_left = np.concatenate((y_tracked_left, y_tracked_left_1))
	y_tracked_right = np.concatenate((y_tracked_right, y_tracked_right_1))

	# for RMSE
	squared_l = np.square(y_target_left - y_tracked_left)
	rm_mean_l = np.sum(squared_l)/squared_l.shape[0]
	root_mean_l = np.sqrt(rm_mean_l)

	squared_r = np.square(y_target_right - y_tracked_right)
	rm_mean_r = np.sum(squared_r)/squared_r.shape[0]
	root_mean_r = np.sqrt(rm_mean_r)

	root_avg = (root_mean_l+ root_mean_r)/2
	if root_avg< min_rmse :
		minC = c
		minQ= Q
		min_rmse= root_avg

	print("C: {:.3f}, Q: {:.3f}, l: {:.3f}, RMSE L :{}".format(c, Q, L,root_mean_l))
	print("C: {:.3f}, Q: {:.3f}, l: {:.3f}, RMSE R :{}".format(c, Q, L,root_mean_r))

print("minC: {:.3f}, minQ: {:.3f}, minRMSE :{}".format(minC, Q, min_rmse))


# file_name1 = "./Tasks/Walk/working_data_2_3/myFile.csv"
# file_name2 = "./Tasks/Walk/working_data_2_3/minimum_points.csv"
# y_target_left_1, y_target_right_1, y_tracked_left_1,y_tracked_right_1 = knee(file_name1, file_name2, Q, L, c)
# y_target_left = np.concatenate((y_target_left, y_target_left_1))
# y_target_right = np.concatenate((y_target_right, y_target_right_1))
# y_tracked_left = np.concatenate((y_tracked_left, y_tracked_left_1))
# y_tracked_right = np.concatenate((y_tracked_right, y_tracked_right_1))

# file_name1 = "./Tasks/Walk/working_data_2_3/myFile.csv"
# file_name2 = "./Tasks/Walk/working_data_2_3/minimum_points.csv"
# y_target_left_1, y_target_right_1, y_tracked_left_1,y_tracked_right_1 = knee(file_name1, file_name2, Q, L, c)
# y_target_left = np.concatenate((y_target_left, y_target_left_1))
# y_target_right = np.concatenate((y_target_right, y_target_right_1))
# y_tracked_left = np.concatenate((y_tracked_left, y_tracked_left_1))
# y_tracked_right = np.concatenate((y_tracked_right, y_tracked_right_1))

# file_name1 = "./Tasks/Walk/working_data_2_3/myFile.csv"
# file_name2 = "./Tasks/Walk/working_data_2_3/minimum_points.csv"
# y_target_left_1, y_target_right_1, y_tracked_left_1,y_tracked_right_1 = knee(file_name1, file_name2, Q, L, c)
# y_target_left = np.concatenate((y_target_left, y_target_left_1))
# y_target_right = np.concatenate((y_target_right, y_target_right_1))
# y_tracked_left = np.concatenate((y_tracked_left, y_tracked_left_1))
# y_tracked_right = np.concatenate((y_tracked_right, y_tracked_right_1))





#control_shell1, runner_pars1 = knee(file_name1 = "./Tasks/Walk/force/myfile.csv", file_name2 = "./Tasks/Walk/force/indx.csv")

#control_shell2, runner_pars2 = knee(file_name = ["walking_test2.csv"])
#for each consecutive step
#modulate dmp to change phi..
#get coupling term from dmp1 and pass to dmp2
#get coupling term from dmp2 and pass to next step of dmp 1
#update step values
# ILC for next trajectory
