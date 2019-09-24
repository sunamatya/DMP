# data_reader
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import peakutils
import pdb
file_name1 = 'all_data/myfile4.csv'
file_name2 = 'all_data/indxR4.csv'

with open(file_name1, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        col_time = []
        col_right = []
        col_left = []
        col_force = []
        for row in reader:#check if all the values are numerical
            #if row[0]=="HS":
            #heelstrike = True
            #row_filter = row[1:]
            row = [float(val) for val in row] #converting them to float
            #col.append(row[1])
            col_time.append(row[0])
            col_right.append(row[2])
            col_left.append(row[1])
            #col_right.append(row[1])
            #col_left.append(row[2])
            col_force.append(row[3])

with open(file_name2, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    col_index = []

    for row in reader:
        row = [int(val) for val in row]
        col_index.append(row[0])

col_index= np.array(col_index)


print(col_index) 

#col_index = np.array([1, 2, 3])      
            
plt.figure(1)
plt.plot(col_time,col_right)
plt.title('Right_Leg')
for i in col_index:
    plt.plot(col_time[i],col_right[i], marker="o", ms=3 )
plt.tight_layout()
plt.show()
# plt.figure(2)
# plt.plot(timestep_left,Encoder_left)
# #plt.plot(time_step,output_signal_force_left)

# plt.title('Left_Leg')
# plt.plot(timestep_left[index_left],Encoder_left[index_left], marker="o", ms=1 )
# plt.tight_layout()

# plt.figure(3)
# plt.plot(time_step,encoderright_flipped)
# plt.title('Right_Leg_flipped')
# plt.plot(time_step[index],encoderright_flipped[index], marker="o", ms=1 )
# plt.tight_layout()    