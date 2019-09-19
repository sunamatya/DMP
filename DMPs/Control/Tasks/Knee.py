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
sys.path.append('/home/student/Documents/DM/DMPs/Control/Controllers')
import os

import Controllers.dmp as DMP
import Controllers.gc as GC
import pdb

import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

def knee(file_name1, file_name2):
    """
    This task sets up the arm to move like a leg walking.

    control_class Control: the controller class chosen for this task
    """

    #--------------------------------
    # set up the rhythmic trajectory that imitates leg walking
    # read in trajectories for each joint from their csv files
    # extract tau from the file
    # extract phi from each files
    #from file read first trajectory
    #one HS to another HS is one trajectory
    #for ii, name in enumerate(names):
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
            col_force.append(row[3])

            # generate function to interpolate the desired trajectory
            '''
            import scipy.interpolate
            path = np.zeros(timesteps)
            # returns evenly spaced numbers over a specific interval
            x = np.linspace(0, 1, len(col))
            #print (x)
            #print ("the length of trajectory is ", len(x))
            #scipy.interpolate.interp1d is used to interpolate a 1D fucntion
            # number of trajectory points
            path_gen = scipy.interpolate.interp1d(x, col)
            '''
    with open(file_name2, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        col_index = []

        for row in reader:
            row = [int(val) for val in row]
            col_index.append(row[0])

    #selection of first gait
    first_gait_left  = col_left[col_index[0]:col_index[1]]
    first_gait_right  = col_right[col_index[0]:col_index[1]]
    second_gait_right = col_right[col_index[1]:col_index[2]]
    #first_gait_right  = np.ones((len(first_gait_right)))*35
    first_force = np.array(col_force[col_index[0]:col_index[1]])
    second_force = np.array(col_force[col_index[1]:col_index[2]])

    timesteps = len(first_gait_right) #+ len(second_gait_right)
    # dt = .01
    # timesteps = int(1./dt) #data access at 100 Hz

    n_joints = 1 # only knee
    trajectory = np.zeros((timesteps+2, n_joints))*np.nan

    # for t in range(timesteps):
    #     path[t] = path_gen(t * dt)
                        #print (path[t])
    # we're only interested in the y-dimensions of each trajectory
    trajectory[1:-1, 0] = np.array(first_gait_right)
    #combined_gait=
    #trajectory[1:len(first_gait_right)+1, 0] = np.array(first_gait_right)
    #trajectory[]
    #pdb.set_trace()
    # for pp, name in enumerate(names):
    plt.figure(1)
    plt.plot(trajectory[1:-1])
    #plt.plot(np.array(col_left))
    plt.title('first_gait_right')
    plt.tight_layout()
    # plt.show()


    #pdb.set_trace()

    # number of goals is the number of (NANs - 1) * number of DMPs
    num_goals = (np.sum(trajectory[:,0] != trajectory[:,0]) - 1) * n_joints
    # respecify goals for spatial scaling by changing add_to_goals
    #n_bfs = [10, 30, 50, 100, 1000]
    n_bfs = [10]
    for ii, bfs in enumerate(n_bfs):
        control_pars = {'add_to_goals':[1e-4]*num_goals,
                        'bfs':bfs, # how many basis function per DMP
                        'gain':100, # pd gain for trajectory following
                        'pattern':'rhythmic', # type of DMP to use
                        'tau':1, # tau is the time scaling term
                        'phi':0, # phi is the change in the term
                        'trajectory':trajectory.T,#transpose
                        'external_force': first_force}

        runner_pars = {'box':[-5,5,-5,5],
                       'control_type':'dmp',
                       'rotate':-np.pi/2.,
                       'title':'Task: Walking'}

        kp = 50 # position error gain on the PD controller
        controller = GC.Control(kp=kp, kv=np.sqrt(kp)) # just sets kp and kv values nothing else
        control_shell = DMP.Shell(controller=controller, **control_pars)


    # A edit
    print("Access after initiate")
    fig_path = './figure'
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    timesteps = control_shell.dmps.timesteps
    dt = 0.01
    external_force = np.zeros((timesteps))

    # Iterate through each gait cycle
    for i in range(5):
        current_gait_right =  np.array(col_right[col_index[i]:col_index[i+1]])
        current_force = np.array(col_force[col_index[i]:col_index[i+1]])
        # Somehow, trajectory isn't used in current formulation for 2nd + gait cycles. Maybe needs a fix.
        path = np.zeros((1, timesteps))
        x = np.linspace(0, control_shell.dmps.cs.run_time, current_gait_right.shape[0]) #linear spacing start, end, number of steps
        path_gen = scipy.interpolate.interp1d(x, current_gait_right) # row by row path generation for each joint
        for t in range(timesteps):
            path[0, t] = path_gen(t * dt)
        y_des = path

        path = np.zeros((timesteps))
        # pdb.set_trace()
        x = np.linspace(0, control_shell.dmps.cs.run_time, current_force.shape[0]) #linear spacing start, end, number of steps
        path_gen = scipy.interpolate.interp1d(x, current_force) # row by row path generation for each joint
        for t in range(timesteps):
            path[t] = path_gen(t * dt)
        # print(np.sum(external_force-path))
        external_force = path
        
        # if i == 0:
        #     f_target = control_shell.dmps.get_target(y_des, external_force)
        #     control_shell.dmps.weight_update(f_target,1,1)
        if i> 0:
            f_target = control_shell.dmps.get_target(y_des, external_force)
            control_shell.dmps.weight_update(f_target,1,0)
        y_track = np.zeros((timesteps))
        dy_track = np.zeros((timesteps))
        ddy_track = np.zeros((timesteps))

        for t in range(timesteps):
            ext= external_force[t]
            # run and record timestep
            y_track[t], dy_track[t], ddy_track[t] = control_shell.dmps.step(external_force= ext, c_a=1, c_v=1)

        # Save first learned trajectory
        if i == 0:
            first_track = np.copy(y_track)

        control_shell.dmps.cs.reset_state()

        plt.figure(i+2)
        #plt.subplot(311)
        plt.plot(y_des[0])
        plt.plot(y_track, label = n_bfs[0])
        plt.plot(first_track)
        plt.legend(loc='lower right')
        plt.legend(['target', 'tracked', 'first'])
        fig_name = '{}/gait_{}.png'.format(fig_path,i+1)
        plt.savefig(fig_name)
    plt.show()

    return (control_shell, runner_pars)
