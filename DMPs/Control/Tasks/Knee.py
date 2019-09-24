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

def knee(file_name1, file_name2, Q, L, c):
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
            #col_right.append(row[1])
            #col_left.append(row[2])
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
    #first_force = np.array(col_force[col_index[0]:col_index[1]])
    

    timesteps = len(first_gait_right) #+ len(second_gait_right)
    first_force  = np.zeros((len(first_gait_right)))
    second_force = np.zeros((len(first_gait_right)))
    #first_force  = np.array(col_force[col_index[0]:col_index[1]])
    #second_force = np.array(col_force[col_index[1]:col_index[2]])
    #timesteps = 629
    # dt = .01
    # timesteps = int(1./dt) #data access at 100 Hz

    n_joints = 1 # only knee
    trajectory = np.zeros((timesteps+2, n_joints))*np.nan
    trajectory2 = np.zeros((timesteps+2, n_joints))*np.nan
    #trajectory[1:-1, 0] = np.sin(np.arange(0, 2*np.pi, .01))


    # for t in range(timesteps):
    #     path[t] = path_gen(t * dt)
                        #print (path[t])
    # we're only interested in the y-dimensions of each trajectory
    #trajectory[1:-1, 0] = np.array(first_gait_right)
    #combined_gait=
    trajectory[1:len(first_gait_right)+1, 0] = np.array(first_gait_right)
    trajectory2[1:len(first_gait_left)+1, 0] = np.array(first_gait_left)
    #trajectory[]
    #pdb.set_trace()
    # for pp, name in enumerate(names):
    plot = False
    if plot == True:
        plt.figure(1)
        plt.subplot(121)
        plt.plot(trajectory[1:-1])
        #plt.plot(np.array(col_left))
        plt.title('first_gait_right')
        plt.subplot(122)
        plt.plot(trajectory2[1:-1])
        #plt.plot(np.array(col_left))
        plt.title('first_gait_left')
        plt.tight_layout()
        # plt.show()



    #pdb.set_trace()

    # number of goals is the number of (NANs - 1) * number of DMPs
    num_goals = (np.sum(trajectory[:,0] != trajectory[:,0]) - 1) * n_joints
    '''
    Testing for code
    '''
    #trajectory = 
    #num_goals = 
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
                        'trajectory':trajectory.T,#transpose
                        'external_force': first_force}

        runner_pars = {'box':[-5,5,-5,5],
                       'control_type':'dmp',
                       'rotate':-np.pi/2.,
                       'title':'Task: Walking'}

        kp = 50 # position error gain on the PD controller
        controller = GC.Control(kp=kp, kv=np.sqrt(kp)) # just sets kp and kv values nothing else
        control_shell = DMP.Shell(controller=controller, **control_pars)


    ##########left_gait###################
    for ii, bfs in enumerate(n_bfs):
        control_pars = {'add_to_goals':[1e-4]*num_goals,
                        'bfs':bfs, # how many basis function per DMP
                        'gain':100, # pd gain for trajectory following
                        'pattern':'rhythmic', # type of DMP to use
                        'tau':1, # tau is the time scaling term
                        'phi':0, # phi is the change in the term
                        'trajectory':trajectory2.T,#transpose
                        'external_force': first_force}

        runner_pars = {'box':[-5,5,-5,5],
                       'control_type':'dmp',
                       'rotate':-np.pi/2.,
                       'title':'Task: Walking'}

        kp = 50 # position error gain on the PD controller
        controller2 = GC.Control(kp=kp, kv=np.sqrt(kp)) # just sets kp and kv values nothing else
        control_shell2 = DMP.Shell(controller=controller2, **control_pars)

    ############### Setting ILC values ############################
    control_shell.dmps.setILC(Q,L,c)
    control_shell2.dmps.setILC(Q,L,c)




    # A edit
    # print("Access after initiate")
    fig_path = './figure'
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    timesteps = control_shell.dmps.timesteps
    dt = 0.01
    external_force = np.zeros((timesteps))

    #Arrays to save output
    #empty holder
    y_target_left = np.zeros((0))
    y_target_right = np.zeros((0))
    y_tracked_left = np.zeros((0))
    y_tracked_right = np.zeros((0))

    # Iterate through each gait cycle
    
    for i in range(len(col_index)-1):
        current_gait_left =  np.array(col_left[col_index[i]:col_index[i+1]])
        current_gait_right =  np.array(col_right[col_index[i]:col_index[i+1]])
        first_gait_right  = np.array(col_right[col_index[0]:col_index[1]])
        first_gait_left = np.array(col_left[col_index[0]:col_index[1]])

        current_force = np.array(col_force[col_index[i]:col_index[i+1]])

        if i >0:
            last_gait_right = np.array(col_right[col_index[i-1]:col_index[i]])
            last_force = np.array(col_force[col_index[i-1]:col_index[i]])
            last_gait_left = np.array(col_left[col_index[i-1]:col_index[i]])



        #current_gait_right = np.sin(np.arange(0, 2*np.pi, .01))
        # Somehow, trajectory isn't used in current formulation for 2nd + gait cycles. Maybe needs a fix.
        
       

        ##############right gait#######################
        path = np.zeros((1, timesteps))
        x = np.linspace(0, control_shell.dmps.cs.run_time, current_gait_right.shape[0]) #linear spacing start, end, number of steps
        path_gen = scipy.interpolate.interp1d(x, current_gait_right) # row by row path generation for each joint
        for t in range(timesteps):
            path[0, t] = path_gen(t * dt)
        y_des = path

        ##############left gait#########################3
        path = np.zeros((1, timesteps))
        x = np.linspace(0, control_shell2.dmps.cs.run_time, current_gait_left.shape[0]) #linear spacing start, end, number of steps
        path_gen = scipy.interpolate.interp1d(x, current_gait_left) # row by row path generation for each joint
        for t in range(timesteps):
            path[0, t] = path_gen(t * dt)
        y_des2 = path

         ################# for the last gait cycle####################

        if i >0:
            path = np.zeros((1, timesteps))
            x = np.linspace(0, control_shell.dmps.cs.run_time, last_gait_right.shape[0]) #linear spacing start, end, number of steps
            path_gen = scipy.interpolate.interp1d(x, last_gait_right) # row by row path generation for each joint
            for t in range(timesteps):
                path[0, t] = path_gen(t * dt)
            y_des_last = path

        if i >0:
            path = np.zeros((1, timesteps))
            x = np.linspace(0, control_shell2.dmps.cs.run_time, last_gait_left.shape[0]) #linear spacing start, end, number of steps
            path_gen = scipy.interpolate.interp1d(x, last_gait_left) # row by row path generation for each joint
            for t in range(timesteps):
                path[0, t] = path_gen(t * dt)
            y_des_last2 = path

        #############for first gaits#####

        path = np.zeros((1, timesteps))
        x = np.linspace(0, control_shell.dmps.cs.run_time, first_gait_right.shape[0]) #linear spacing start, end, number of steps
        path_gen = scipy.interpolate.interp1d(x, first_gait_right) # row by row path generation for each joint
        for t in range(timesteps):
            path[0, t] = path_gen(t * dt)
        first = path

        path = np.zeros((1, timesteps))
        x = np.linspace(0, control_shell2.dmps.cs.run_time, first_gait_left.shape[0]) #linear spacing start, end, number of steps
        path_gen = scipy.interpolate.interp1d(x, first_gait_left) # row by row path generation for each joint
        for t in range(timesteps):
            path[0, t] = path_gen(t * dt)
        first2 = path

        path = np.zeros((timesteps))
        # pdb.set_trace()
        x = np.linspace(0, control_shell.dmps.cs.run_time, current_force.shape[0]) #linear spacing start, end, number of steps
        path_gen = scipy.interpolate.interp1d(x, current_force) # row by row path generation for each joint
        for t in range(timesteps):
            path[t] = path_gen(t * dt)
        # print(np.sum(external_force-path))
        external_force = path

   
        #################################################

        if i >0 : 
            path = np.zeros((timesteps))
            # pdb.set_trace()
            x = np.linspace(0, control_shell.dmps.cs.run_time, last_force.shape[0]) #linear spacing start, end, number of steps
            path_gen = scipy.interpolate.interp1d(x, last_force) # row by row path generation for each joint
            for t in range(timesteps):
                path[t] = path_gen(t * dt)
            # print(np.sum(external_force-path))
            external_force_last = path
        # else:
        #      path = np.zeros((timesteps))
        #     # pdb.set_trace()
        #     x = np.linspace(0, control_shell.dmps.cs.run_time, last_force.shape[0]) #linear spacing start, end, number of steps
        #     path_gen = scipy.interpolate.interp1d(x, last_force) # row by row path generation for each joint
        #     for t in range(timesteps):
        #         path[t] = path_gen(t * dt)
        #     # print(np.sum(external_force-path))
        #     external_force_last = path






        if i == 0:
            external_force = np.zeros((timesteps))
            f_target = control_shell.dmps.get_target(y_des, ext_force= None)
            #control_shell.dmps.weight_update(f_target,r =1)
            control_shell.dmps.batch_regression(f_target = f_target,r = 1)

            external_force = np.zeros((timesteps))
            f_target2 = control_shell2.dmps.get_target(y_des2, ext_force= None)
            #control_shell.dmps.weight_update(f_target,r =1)
            control_shell2.dmps.batch_regression(f_target = f_target2,r = 1)


       
        if i  > 0:
            f_target = control_shell.dmps.get_target(y_des = y_des_last, ext_force = external_force)
            #f_target = control_shell.dmps.get_target(y_des = first, ext_force = external_force)
            control_shell.dmps.weight_update(f_target = f_target,r = 1)

            f_target2 = control_shell2.dmps.get_target(y_des = y_des_last2, ext_force = external_force)
            #f_target = control_shell.dmps.get_target(y_des = first, ext_force = external_force)
            control_shell2.dmps.weight_update(f_target = f_target2,r = 1)

            

        y_track = np.zeros((timesteps))
        dy_track = np.zeros((timesteps))
        ddy_track = np.zeros((timesteps))

        y_track2 = np.zeros((timesteps))
        dy_track2 = np.zeros((timesteps))
        ddy_track2 = np.zeros((timesteps))


        if i == 0:
            for t in range(timesteps):
                #ext= external_force[t]
                #ext= external_force_last[t]
                # run and record timestep
                y_track[t], dy_track[t], ddy_track[t] = control_shell.dmps.step(external_force= None, c_a=1, c_v=1, t_s=t, firstgait=True)
                y_track2[t], dy_track2[t], ddy_track2[t] = control_shell2.dmps.step(external_force= None, c_a=1, c_v=1, t_s=t, firstgait=True)

        if i  > 0:
            for t in range(timesteps):
                ext= external_force[t]
                #ext= external_force_last[t]
                # run and record timestep
                y_track[t], dy_track[t], ddy_track[t] = control_shell.dmps.step(external_force= ext, c_a=1, c_v=1, t_s=t)
                #y_track[t], dy_track[t], ddy_track[t] = control_shell.dmps.step(external_force= None, c_a=1, c_v=1, t_s = t)
                y_track2[t], dy_track2[t], ddy_track2[t] = control_shell2.dmps.step(external_force= ext, c_a=1, c_v=1, t_s=t)

        # else:
        #     for t in range(timesteps):
        #         #ext= external_force[t]
        #         ext= external_force_last[t]
        #         # run and record timestep
        #         y_track[t], dy_track[t], ddy_track[t] = control_shell.dmps.step(external_force= ext, c_a=1, c_v=1, t_s=t)
        #         #y_track[t], dy_track[t], ddy_track[t] = control_shell.dmps.step(external_force= None, c_a=1, c_v=1, t_s = t)
        # # Save first learned trajectory
        if i == 0:
            first_track = np.copy(y_track)
            first_track2 = np.copy(y_track2)

        control_shell.dmps.cs.reset_state()
        control_shell2.dmps.cs.reset_state()

        ###saving data for RMSE########
        y_target_left = np.concatenate((y_target_left, y_des2[0]))
        y_target_right = np.concatenate((y_target_right, y_des[0]))
        y_tracked_left = np.concatenate((y_tracked_left, y_track2))
        y_tracked_right = np.concatenate((y_tracked_right, y_track))


        if (plot == True):

            plt.figure(i+2)
            #plt.subplot(311)
            plt.subplot(121)
            plt.plot(y_des[0])
            plt.plot(y_track)
            #plt.plot(y_track, label = n_bfs[0])
            plt.plot(first_track)
            if i>0:
                plt.plot(y_des_last[0])
            plt.legend(loc='lower right')
            plt.legend(['target', 'tracked', 'first', 'last'])
            plt.subplot(122)
            plt.plot(y_des2[0])
            plt.plot(y_track2)
            #plt.plot(y_track, label = n_bfs[0])
            plt.plot(first_track2)
            if i>0:
                plt.plot(y_des_last2[0])

            plt.legend(loc='lower right')
            plt.legend(['target', 'tracked', 'first', 'last'])

            fig_name = '{}/gait_{}.png'.format(fig_path,i+1)
            plt.title(i)

            plt.savefig(fig_name)

    if (plot== True):
        plt.show()

    return (y_target_left, y_target_right, y_tracked_left,y_tracked_right)
