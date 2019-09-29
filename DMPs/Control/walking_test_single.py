# test the dmp
import sys
sys.path.append('/home/student/Documents/DM/DMPs/Control')
sys.path.append('/home/student/Documents/DM/DMPs/Control/Controllers')



import Controllers.dmp as dmp  # import the dmp for controller
#import Tasks.walk as walk # import the walking data for trajectory
#import Tasks.knee as walk # import the walking data for trajectory
from Tasks.Knee import knee
from Tasks.Knee_backup import knee_backup

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
#file_name1 = "./Tasks/all_data/karishma_me/myfile21.csv"
#file_name2 = "./Tasks/all_data/karishma_me/indx_K21_L.csv"

y_target_left, y_target_right, y_tracked_left,y_tracked_right, interpolated_time, avg_left_target, avg_right_target, avg_left_tracked, avg_right_tracked = knee(file_name1, file_name2, Q, L, c)

squared_l = np.square(y_target_left - y_tracked_left)
rm_mean_l = np.sum(squared_l)/squared_l.shape[0]
root_mean_l = np.sqrt(rm_mean_l)

max_error_l = np.max(np.abs(y_target_left - y_tracked_left))
#mean_error_l = np.sum(max_error_l)/max_error_l.shape[0]

squared_r = np.square(y_target_right - y_tracked_right)
rm_mean_r = np.sum(squared_r)/squared_r.shape[0]
root_mean_r = np.sqrt(rm_mean_r)

max_error_r = np.max(np.abs(y_target_right - y_tracked_right))
#mean_error_r = np.sum(max_error_r)/max_error_r.shape[0]


root_avg = (root_mean_l+ root_mean_r)/2


# print("C: {:.3f}, Q: {:.3f}, RMSE L :{}".format(c, Q, root_mean_l))
# print("C: {:.3f}, Q: {:.3f}, RMSE R :{}".format(c, Q, root_mean_r))
# print("C: {:.3f}, Q: {:.3f}, MAX_ERROR L :{}".format(c, Q, max_error_l))
# print("C: {:.3f}, Q: {:.3f}, MAX_ERROR R :{}".format(c, Q, max_error_r ))
y_target_left2, y_target_right2, y_tracked_left2,y_tracked_right2, interpolated_time2, avg_left_target2, avg_right_target2, avg_left_tracked2, avg_right_tracked2 = knee_backup(file_name1, file_name2, Q, L, c)

#interpolated_time = np.arange(y_target_left.shape[0])/1000
squared_l2 = np.square(y_target_left2 - y_tracked_left2)
rm_mean_l2 = np.sum(squared_l2)/squared_l2.shape[0]
root_mean_l2 = np.sqrt(rm_mean_l2)

max_error_l2 = np.max(np.abs(y_target_left2 - y_tracked_left2))

squared_r2 = np.square(y_target_right2 - y_tracked_right2)
rm_mean_r2 = np.sum(squared_r2)/squared_r2.shape[0]
root_mean_r2 = np.sqrt(rm_mean_r2)

max_error_r2 = np.max(np.abs(y_target_right2 - y_tracked_right2))

root_avg2 = (root_mean_l2+ root_mean_r2)/2


# print("C: {:.3f}, Q: {:.3f}, RMSE L :{}".format(c, Q, root_mean_l2))
# print("C: {:.3f}, Q: {:.3f}, RMSE R :{}".format(c, Q, root_mean_r2))
# print("C: {:.3f}, Q: {:.3f}, MAX_ERROR L :{}".format(c, Q, max_error_l2))
# print("C: {:.3f}, Q: {:.3f}, MAX_ERROR R :{}".format(c, Q, max_error_r2))
#######plot for results############

import matplotlib.pyplot as plt

plt.figure(1)

plt.subplot(121)
plt.plot(interpolated_time, y_target_left)
plt.plot(interpolated_time, y_tracked_left, '--')
plt.plot(interpolated_time, y_tracked_left2, '-.')
plt.legend(loc='upper left')
plt.legend(['target', 'Baseline', 'Co-operative DMP'])
plt.xlabel('time(sec)',fontweight ='bold')
plt.ylabel('Left Knee Joint Angle (deg)',fontweight ='bold')


#plt.title('Left Leg Gait')
plt.subplot(122)
plt.plot(interpolated_time, y_target_right)
plt.plot(interpolated_time, y_tracked_right, '--')
plt.plot(interpolated_time, y_tracked_right2, '-.')
#plt.title('Right Leg Gait')
#plt.legend(loc='upper right')
#plt.legend(['target', 'Baseline', 'Co-operative DMP'])
plt.xlabel('time(sec)', fontweight ='bold',fontsize =12)
plt.ylabel('Right Knee Joint Angle (deg)', fontweight ='bold')

#plt.legend(['target', 'Batch regression', 'ILWR + ILC'])


plt.tight_layout()
plt.savefig("Sun_Tan_1.png")
plt.show()
x = np.arange(0,1, 1/628.)
print(x.shape)
print(avg_left_target.shape)

plt.figure(2)

plt.subplot(121)
plt.plot(x, avg_left_target)
plt.plot(x, avg_left_tracked, '--')
plt.plot(x, avg_left_tracked2, '-.')
plt.legend(loc='upper left')
plt.legend(['target', 'Baseline', 'Co-operative DMP'])
plt.xlabel('time(sec)',fontweight ='bold')
plt.ylabel('Knee Joint Angle (deg)',fontweight ='bold')




#plt.title('Left Leg Gait')
plt.subplot(122)
plt.plot(x, avg_right_target)
plt.plot(x, avg_right_tracked, '--')
plt.plot(x, avg_right_tracked2, '-.')
#plt.title('Right Leg Gait')
plt.xlabel('timesteps', fontweight ='bold',fontsize =12)
plt.ylabel('Knee Joint Angle (deg)', fontweight ='bold')
#plt.legend(loc='upper right')
#plt.legend(['target', 'Batch regression', 'ILWR + ILC'])


plt.tight_layout()
plt.savefig("Sun_Tan_avg_1.png")
plt.show()

plt.figure(3)
plt.plot(x,avg_left_target)
plt.plot(x,avg_left_tracked, '--')
plt.plot(x, avg_left_tracked2, '-.')
plt.legend(loc='upper left')
plt.legend(['target', 'Baseline', 'Co-operative DMP'])
plt.xlabel('timesteps',fontweight ='bold')
plt.ylabel('Knee Joint Angle (deg)',fontweight ='bold')


plt.tight_layout()
plt.savefig("Sun_Tan_avg_left_1.png")
plt.show()

plt.figure(4)
plt.plot(interpolated_time, y_target_right)
plt.plot(interpolated_time, y_tracked_right, '--')
plt.plot(interpolated_time, y_tracked_right2, '-.')
#plt.title('Right Leg Gait')
#plt.legend(loc='upper right')
#plt.legend(['target', 'Baseline', 'Co-operative DMP'])
plt.legend(loc='upper right')
plt.legend(['target', 'Baseline', 'Co-operative DMP'])
plt.xlabel('time(sec)', fontweight ='bold',fontsize =12)
plt.ylabel('Right Knee Joint Angle (deg)', fontweight ='bold')


plt.tight_layout()
plt.savefig("Pair1_epoch1.png")
plt.show()


#fontsize =12
# import matplotlib.pyplot as plt
# plt.figure(1)
# plt.subplot(121)
# plt.plot(y_target_left)
# plt.plot(y_tracked_left, '--')
# plt.xlabel('t (s)')
# plt.ylabel('Knee Joint Angle (deg)')
# plt.legend(loc='upper right')
# plt.legend(['target', 'tracked'])
# plt.title('Left Leg Gait')
# plt.subplot(122)
# plt.plot(y_target_right)
# plt.plot(y_tracked_right, '--')
# plt.title('Right Leg Gait')
# plt.xlabel('t (s)')
# plt.ylabel('Knee Joint Angle (deg)')
# plt.legend(loc='upper right')
# plt.legend(['target', 'tracked'])
# plt.tight_layout()
# plt.savefig("shit_data.png")
# plt.show()

