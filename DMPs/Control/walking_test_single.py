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
#minC: 0.100, minQ: 0.900, minRMSE :3.6581161009738246

#tanishka data 1
#minC: 0.100, minQ: 0.900, minRMSE :5.149932448507941
#minC: 0.100, minQ: 0.900, minRMSE :8.267959003331454



Q = 0.9
L = 0.1
c = 0.1

#file_name1 = "./Tasks/Walk/working_data_2_3/myFile.csv"
#file_name2 = "./Tasks/Walk/working_data_2_3/minimum_points.csv"

file_name1 = "./Tasks/fwddata/myfile_TS1.csv"
file_name2 = "./Tasks/fwddata/indx_TS1_L.csv"

y_target_left, y_target_right, y_tracked_left,y_tracked_right, interpolated_time = knee(file_name1, file_name2, Q, L, c)

squared_l = np.square(y_target_left - y_tracked_left)
rm_mean_l = np.sum(squared_l)/squared_l.shape[0]
root_mean_l = np.sqrt(rm_mean_l)

squared_r = np.square(y_target_right - y_tracked_right)
rm_mean_r = np.sum(squared_r)/squared_r.shape[0]
root_mean_r = np.sqrt(rm_mean_r)

root_avg = (root_mean_l+ root_mean_r)/2


#print("C: {:.3f}, Q: {:.3f}, RMSE L :{}".format(c, Q, root_mean_l))
#print("C: {:.3f}, Q: {:.3f}, RMSE R :{}".format(c, Q, root_mean_r))\



#######plot for results############

import matplotlib.pyplot as plt
plt.figure(1)
plt.subplot(121)
plt.plot(interpolated_time, y_target_left)
plt.plot(interpolated_time, y_tracked_left, '--')
plt.xlabel('t (s)')
plt.ylabel('Knee Joint Angle (deg)')
plt.legend(loc='upper right')
plt.legend(['target', 'tracked'])
plt.title('Left Leg Gait')
plt.subplot(122)
plt.plot(interpolated_time, y_target_right)
plt.plot(interpolated_time, y_tracked_right, '--')
plt.title('Right Leg Gait')
plt.xlabel('t (s)')
plt.ylabel('Knee Joint Angle (deg)')
plt.legend(loc='upper right')
plt.legend(['target', 'tracked'])
plt.tight_layout()
plt.savefig("dataTS1_dmp.png")
plt.show()

