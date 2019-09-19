import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import peakutils
import pdb

spamReader = csv.reader(open('Walk/Data_Karishma_Sunny/GRF_F_2_3.txt', 'r'), delimiter=',')
sensor_1 = []
time_step = []
sensor_2 = []
sensor_3 = []
sensor_4= []
sensor_5 = []
sensor_6=[]
sensor_7 = []
sensor_8 = []
Encoder_right = []
Force_data = []
next(spamReader)# to not read header
for row in spamReader:
	#print(row[0]) # this is date time
	# this is encoder data
	#print(row[11])
	#row[1] =float(row[1])
	#row[0]= 2019-09-06 19:09:15.021284
	# 0               1     2  3  4  5  6  7  8  9  10,  11
	#time_index,time_stamp,L1,L2,L3,L4,R1,R2,R3,R4,Futek,ENC2
	if (len(row)< 12):
		continue
	ctime = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f")
	ctime = datetime.timestamp(ctime)
	time_step.append(ctime)

	Encoder_right.append((float(row[11])+10)*360.0/500.0) #offset

	
	sensor_1.append(float(row[2])-200)
	sensor_5.append(float(row[6])-200)

time_step = np.array(time_step)
Encoder_right = np.array(Encoder_right)
index = []
encoderright_flipped = np.min(Encoder_right)-Encoder_right
index = peakutils.indexes(encoderright_flipped, thres=0.1, min_dist=5)


#print(index)
#print(output_signal_force_left[index])

Encoder_left = []
timestep_left = []
spamReader2 = csv.reader(open('Walk/Data_Karishma_Sunny/Encoder2_3.txt', 'r'), delimiter=',')
next(spamReader2)# to not read header
for row in spamReader2:
	#print(row[0]) # this is date time
	# this is encoder data
	#print(row[1])
	#row[1] =float(row[1])
	#row[0]= 2019-09-06 19:09:15.021284
	#time_index,time_stamp,L1,L2,L3,L4,R1,R2,R3,R4,Futek,ENC2
	ctime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
	ctime = datetime.timestamp(ctime)
	timestep_left.append(ctime)
	Encoder_left.append(float(row[1])*360.0/500.0)

timestep_left = np.array(timestep_left)
Encoder_left = np.array(Encoder_left)

index_left = []
encoderleft_flipped = np.min(Encoder_left)-Encoder_left
index_left = peakutils.indexes(encoderleft_flipped, thres=0.1, min_dist=5)

###################################IMU Data#####################################

#IMU1_3 = []
timestep_IMU = []
spamReader3 = csv.reader(open('Walk/Data_Karishma_Sunny/IMU2_3.txt', 'r'), delimiter=',')
#next(spamReader3)# to not read header
for row in spamReader3:
	#print(row[0]) # this is date time
	# this is encoder data
	#print(row[1])
	#row[1] =float(row[1])
	#row[0]= 2019-09-06 19:09:15.021284
	#time_index,time_stamp,L1,L2,L3,L4,R1,R2,R3,R4,Futek,ENC2
	ctime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
	ctime = datetime.timestamp(ctime)
	timestep_IMU.append(ctime)
	
timestep_IMU = np.array(timestep_IMU)
print(timestep_IMU)

#######################################Force Data#####################################

#spamReader3 = csv.reader(open('Walk/Data_Karishma_Sunny/Force.csv', 'r'), delimiter=',')
#next(spamReader3)# to not read header
#for row in spamReader3:
	#print(row[0]) # this is date time
	# this is encoder data
	#print(row[1])
	#row[1] =float(row[1])
	#row[0]= 2019-09-06 19:09:15.021284
	#time_index,time_stamp,L1,L2,L3,L4,R1,R2,R3,R4,Futek,ENC2
#	ctime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
#	ctime = datetime.timestamp(ctime)
#	timestep_left.append(ctime)
#	Encoder_left.append(float(row[1])*360.0/500.0)
#	Force_data.append(float(row[10]))
'''
print(len(index))
print(index[0])
pdb.set_trace()
print(time_step[np.array(index,int)])
print(Encoder_right[np.array(index, int)])
exit()
'''

plt.figure(1)
plt.plot(time_step,Encoder_right)
plt.title('Right_Leg')
plt.plot(time_step[index],Encoder_right[index], marker="o", ms=1 )
plt.tight_layout()
#plt.show()
plt.figure(2)
plt.plot(timestep_left,Encoder_left)
#plt.plot(time_step,output_signal_force_left)

plt.title('Left_Leg')
plt.plot(timestep_left[index_left],Encoder_left[index_left], marker="o", ms=1 )
plt.tight_layout()

plt.figure(3)
plt.plot(time_step,encoderright_flipped)
plt.title('Right_Leg_flipped')
plt.plot(time_step[index],encoderright_flipped[index], marker="o", ms=1 )
plt.tight_layout()


# this is mock part to make csv file with time for both legs

writer_test_1= open('right_leg_2_3.csv', 'w')

with writer_test_1:

    writer = csv.writer(writer_test_1)
    for i in range(time_step.shape[0]):
    	writer.writerow((time_step[i],Encoder_right[i]))

writer_test_2= open('left_leg_2_3.csv', 'w')
with writer_test_2:

    writer = csv.writer(writer_test_2)
    for i in range(timestep_left.shape[0]):
    	writer.writerow((timestep_left[i],Encoder_left[i]))


writer_test_3= open('imu2_3_time.csv', 'w')
with writer_test_3:

    writer = csv.writer(writer_test_3)
    for i in range(timestep_IMU.shape[0]):
    	writer.writerow((timestep_IMU[i],Encoder_left[i]))

#plt.figure(1)
#plt.plot(time_step,output_signal_force_right)
#plt.title('Right_Leg')
#plt.tight_layout()
#plt.show()

#plt.figure(3)
#plt.plot(time_step,Force_data)
#plt.title('Interaction_force')
#plt.tight_layout()



plt.show()
plt.close("all")
'''
plt.figure(1)
plt.plot(time_step,sensor_1)
plt.title('testing_1')
plt.tight_layout()
#plt.show()

plt.figure(2)
plt.plot(time_step,sensor_2)
plt.title('testing_2')
plt.tight_layout()
#plt.show()

plt.figure(3)
plt.plot(time_step,sensor_3)
plt.title('testing_3')
plt.tight_layout()
plt.show()

plt.figure(4)
plt.plot(time_step,sensor_4)
plt.title('testing_4')
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(time_step,sensor_5)
plt.title('testing_5')
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(time_step,sensor_6)
plt.title('testing_6')
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(time_step,sensor_7)
plt.title('testing_7')
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(time_step,sensor_8)
plt.title('testing_8')
plt.tight_layout()
plt.show()
'''

    
	#if (isinstance(row, datetime.datetime)):
	#print('//'.join(row))
