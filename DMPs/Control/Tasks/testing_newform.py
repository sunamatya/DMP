import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import peakutils

spamReader = csv.reader(open('Walk/KASHAYAP/F_22.txt', 'r'), delimiter=',')
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
Encoder_left = []
next(spamReader)# to not read header
for row in spamReader:
	#row[0]= 2019-09-06 19:09:15.021284
	# 0       1     2 		 3 4  5  6  7 
	#Ttime, Futek, ENCL, ENCR, X, Y, Z, W 
	time_step.append(Ttime)
	Encoder_right.append((float(row[3])+90)*360.0/500.0)
	#time_step.append(Ttime)
	Encoder_left.append((float(row[2])+90)*360.0/500.0)







plt.figure(1)
plt.plot(time_step,Encoder_right)
plt.title('Right_Leg')
plt.tight_layout()
#plt.show()
plt.figure(2)
plt.plot(timestep_left,Encoder_left)
plt.plot(time_step,output_signal_force_left)
plt.plot(time_step[index],output_signal_force_left[index], marker="o", ms=3 )
plt.title('Left_Leg')
plt.tight_layout()



plt.show()
plt.close("all")
'''
