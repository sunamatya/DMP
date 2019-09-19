import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

Fs = 100; #100 Hz
SimulationTime = 10; # read from file
T = 1/Fs; # sampling time

# extract oscillator data
M = 5 # number of components in Fourier series
K = 20 # coupling strength
eta = 1 # learning constant
#phi = self.phi # phi is phase of the oscillator # extract from data
#Omega = self.Omega # Omega denotes frequencyphi = self.phi # phi is phase of the oscillator # extract from data

phi = self.phi # phi is phase of the oscillator # extract from data
Omega = 2 # Omega denotes frequencyphi = self.phi # phi is phase of the oscillator # extract from data

#for ii in range(self.num_seqs):
#c= 0 to M
# initializing alpha 
alpha = np.array([1, 1, 1, 1, 1])

for t in range(SimulationTime):

	for c in range(M):
		y_hat = y_hat + (alpha[c]* cos(c*phi))

	e_0 = y_demo -y_hat

	for c in range(M):
		d_alpha= eta*cos(c*phi)*e_0
		alpha[c] = alpha[c]+ d_alpha*T
		
	phi_d = Omega - K *e_0*(sin(phi))
	Omega_d = -K *e_0*(sin(phi))
	Omega = Omega + T*Omega_d


#for n in range(SimulationTime)


# get the ii'th sequence


