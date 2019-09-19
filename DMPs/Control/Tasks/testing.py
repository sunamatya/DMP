
output_signal_force_right= signal.filtfilt(b, a, sensor_5)
index = []
index = peakutils.indexes(output_signal_force_left, thres=0.1, min_dist=10)


Encoder_left = []
timestep_left = []
spamReader2 = csv.reader(open('Walk/Data_Karishma_Sunny/Encoder1_4.txt', 'r'), delimiter=',')
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

plt.figure(1)
plt.plot(time_step,Encoder_right)
plt.title('Right_Leg')
plt.tight_layout()
#plt.show()
plt.figure(2)
plt.plot(timestep_left,Encoder_left)
plt.plot(time_step,output_signal_force_left)
plt.plot(output_signal_force_left[index], marker="o", ls="", ms=3 )
plt.title('Left_Leg')
plt.tight_layout()


plt.figure(1)
plt.plot(time_step,output_signal_force_right)
plt.title('Right_Leg')
plt.tight_layout()
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
