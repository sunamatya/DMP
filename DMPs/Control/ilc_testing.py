from __future__ import division
import sys
import numpy as np

Q = 0.99 # positive scalars
L = 1 # positive scalars
c = 0.5 # learning from present 

    
	#ILC from LPV
    #temp_u=kp*self.th_e+ kd*(self.e[i+1]-self.e[i])
    #FC-i = Coupled Learned Force, current iteraton learning control
    e_i = -self.interaction_force

    FC_i = Q*(FC_i+ L*c*e_dot)
    C_i = c*e_i+ FC_i

    # make RBF with x... same as f(x)
    # a through least sqaure sense?? how.. check