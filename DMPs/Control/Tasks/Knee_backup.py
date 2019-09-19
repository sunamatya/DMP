'''
Copyright (C) 2014 Travis DeWolf

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import sys
sys.path.append('/home/labuser/Documents/DM/DMPs/Control/Controllers')

import Controllers.dmp as DMP
import Controllers.gc as GC
import pdb

import csv
import numpy as np
import matplotlib.pyplot as plt
def knee(file_name):
    """
    This task sets up the arm to move like a leg walking.

    control_class Control: the controller class chosen for this task
    """

    #--------------------------------
    # set up the rhythmic trajectory that imitates leg walking
    # read in trajectories for each joint from their csv files
    # extract tau from the file
    # extract phi from each files
    dt = .01
    timesteps = int(1./dt)
    #names = ['hip_traj.csv', 'knee_traj.csv', 'ankle_traj.csv']
    #names = ['knee.csv']
    names = file_name
    n_joints = len(names)
    trajectory = np.zeros((timesteps+2, n_joints))*np.nan

    #from file read first trajectory
    #one HS to another HS is one trajectory
    for ii, name in enumerate(names):
        with open('Tasks/Walk/'+name, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            col = []
            for row in reader:#check if all the values are numerical
                #if row[0]=="HS": 
                #heelstrike = True
                #row_filter = row[1:] 
                row = [float(val) for val in row] #converting them to float
                #col.append(row[1])
                col.append(row[0])
            
            # generate function to interpolate the desired trajectory
            import scipy.interpolate
            path = np.zeros(timesteps)
            # returns evenly spaced numbers over a specific interval
            x = np.linspace(0, 1, len(col))
            #print (x)
            #print ("the length of trajectory is ", len(x))
            #scipy.interpolate.interp1d is used to interpolate a 1D fucntion
            # number of trajectory points
            path_gen = scipy.interpolate.interp1d(x, col)   


            
            for t in range(timesteps):  
                path[t] = path_gen(t * dt)
                                #print (path[t])
            # we're only interested in the y-dimensions of each trajectory
            trajectory[1:-1, ii] = path

    for pp, name in enumerate(names):        
        plt.figure()
        plt.plot(trajectory[1:101,pp])
        plt.title(name)
        plt.tight_layout()
        #plt.show()
    

    #pdb.set_trace()

    # number of goals is the number of (NANs - 1) * number of DMPs
    num_goals = (np.sum(trajectory[:,0] != trajectory[:,0]) - 1) * n_joints
    # respecify goals for spatial scaling by changing add_to_goals
    #n_bfs = [10, 30, 50, 100, 1000]
    n_bfs = [100]
    for ii, bfs in enumerate(n_bfs):
        control_pars = {'add_to_goals':[1e-4]*num_goals,
                        'bfs':bfs, # how many basis function per DMP
                        'gain':100, # pd gain for trajectory following
                        'pattern':'rhythmic', # type of DMP to use
                        'tau':1, # tau is the time scaling term
                        'phi':0, # phi is the change in the term
                        'trajectory':trajectory.T,} #transpose

        runner_pars = {'box':[-5,5,-5,5],
                       'control_type':'dmp',
                       'rotate':-np.pi/2.,
                       'title':'Task: Walking'}

        kp = 50 # position error gain on the PD controller
        controller = GC.Control(kp=kp, kv=np.sqrt(kp)) # just sets kp and kv values nothing else
        control_shell = DMP.Shell(controller=controller, **control_pars)

    return (control_shell, runner_pars)
