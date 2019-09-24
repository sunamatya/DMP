import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

#def adaptive_oscillator():


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    Fs = 1000
    Tfinal = 10.0
    T = 1/Fs
    t = np.linspace(0, Tfinal, Tfinal/T, endpoint=True)

    plotvar1 = np.linspace(0,0,Tfinal/T);
	plotvar2 = np.linspace(0,0,Tfinal/T);
	plotvar3 = np.linspace(0,0,Tfinal/T);

    x = 1 # starting point of the oscillator
    x_new = 0
    x_d = 0
    y = 0
    y_new - 0
    y_d = 0
    ohm = 10*2*pi #10 Hz 
    ohm_new = 0
    ohm_d = 0

    Epsilon = 15

    gamma = 100

    mu = 1.0

    for i in range(Tfinal/T):
    	if i < Tfinal/(4*T):
    		F = 0
    	elif i > Tfinal/(4*T/3) and :
    		F =  np.sin(12.5*2*np.pi*n*T) #12.5 Hz
    	elif i > 


x = np.linspace(-np.pi, np.pi, 201)
>>> plt.plot(x, np.sin(x))
>>> plt.xlabel('Angle [rad]')
>>> plt.ylabel('sin(x)')
>>> plt.axis('tight')
>>> plt.show()
