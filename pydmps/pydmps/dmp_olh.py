'''
Copyright (C) 2013 Travis DeWolf

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
import numpy as np

from pydmps.cs import CanonicalSystem
import pdb

class DMPs(object):
    """Implementation of Dynamic Motor Primitives,
    as described in Dr. Stefan Schaal's (2002) paper."""

    def __init__(self, n_dmps, n_bfs, dt=.01,
                 y0=0, goal=1, w=None,
                 ay=None, by=None, external_force=None, **kwargs):
        """
        n_dmps int: number of dynamic motor primitives
        n_bfs int: number of basis functions per DMP
        dt float: timestep for simulation
        y0 list: initial state of DMPs
        goal list: goal state of DMPs
        w list: tunable parameters, control amplitude of basis functions
        ay int: gain on attractor term y dynamics
        by int: gain on attractor term y dynamics
        """
        #print("dmp, pydmps", external_force.shape)
        #print("dmp, pydmps", kwargs.keys())
        self.n_dmps = n_dmps
        self.n_bfs = n_bfs #1000
        self.dt = dt# 0.01
        if isinstance(y0, (int, float)):
            y0 = np.ones(self.n_dmps)*y0
        self.y0 = y0
        if isinstance(goal, (int, float)):
            goal = np.ones(self.n_dmps)*goal
        self.goal = goal
        if w is None:
            # default is f = 0
            w = np.zeros((self.n_dmps, self.n_bfs))
        self.w = w

        self.ay = np.ones(n_dmps) * 25. if ay is None else ay  # Schaal 2012
        self.by = self.ay / 4. if by is None else by  # Schaal 2012

        # set up the CS
        self.cs = CanonicalSystem(dt=self.dt, **kwargs)
        self.timesteps = int(self.cs.run_time / self.dt)


        # set up the DMP system
        self.reset_state()
        self.data_path = None

        self.external_force = external_force
        self.w_p = np.zeros((self.timesteps, self.n_bfs))

        # this is for ILC
        self.FC_i = 0 # coupling learned force
        self.e_i = 0

        #this is for linear propagation
        #self.P = np.ones((self.timesteps, self.n_bfs))
        self.P = np.ones((self.timesteps, self.n_bfs))
        self.error = np.zeros((self.timesteps, self.n_bfs))

    def check_offset(self):
        """Check to see if initial position and goal are the same
        if they are, offset slightly so that the forcing term is not 0"""

        for d in range(self.n_dmps):
            if (self.y0[d] == self.goal[d]):
                self.goal[d] += 1e-4

    def gen_front_term(self, x, dmp_num):
        raise NotImplementedError()

    def gen_goal(self, y_des):
        raise NotImplementedError()

    def gen_psi(self):
        raise NotImplementedError()

    def gen_weights(self, f_target):
        raise NotImplementedError()

    def imitate_path(self, y_des, plot=False):
        """Takes in a desired trajectory and generates the set of
        system parameters that best realize this path.

        y_des list/array: the desired trajectories of each DMP
                          should be shaped [n_dmps, run_time]
        """

        # set initial state and goal
        if y_des.ndim == 1:
            y_des = y_des.reshape(1, len(y_des))
        self.y0 = y_des[:, 0].copy()
        self.y_des = y_des.copy()
        self.goal = self.gen_goal(y_des)
        #self.goal = np.array([25.92])
        print (self.goal)

        self.check_offset()

        # generate function to interpolate the desired trajectory
        import scipy.interpolate
        path = np.zeros((self.n_dmps, self.timesteps))
        x = np.linspace(0, self.cs.run_time, y_des.shape[1]) #linear spacing start, end, number of steps
        for d in range(self.n_dmps):
            path_gen = scipy.interpolate.interp1d(x, y_des[d]) # row by row path generation for each joint
            for t in range(self.timesteps):
                path[d, t] = path_gen(t * self.dt)
        y_des = path

        # calculate velocity of y_des
        dy_des = np.diff(y_des) / self.dt
        # add zero to the beginning of every row
        dy_des = np.hstack((np.zeros((self.n_dmps, 1)), dy_des))

        # calculate acceleration of y_des
        ddy_des = np.diff(dy_des) / self.dt
        # add zero to the beginning of every row
        ddy_des = np.hstack((np.zeros((self.n_dmps, 1)), ddy_des))

        f_target = np.zeros((y_des.shape[1], self.n_dmps))
        # find the force required to move along this trajectory

        import scipy.interpolate
        path = np.zeros((self.timesteps))
        #if external_force is not None:
        x = np.linspace(0, self.cs.run_time, self.external_force.shape[0]) #linear spacing start, end, number of steps

        path_gen = scipy.interpolate.interp1d(x, self.external_force) # row by row path generation for each joint
        for t in range(self.timesteps):
            path[t] = path_gen(t * self.dt)

        self.external_force = path
        for d in range(self.n_dmps):
            f_target[:, d] = (ddy_des[d] - self.ay[d] *
                              (self.by[d] * (self.goal[d] - y_des[d]) -
                              dy_des[d])-self.external_force)
            #need to add coupling term here

        # efficiently generate weights to realize f_target
        self.gen_weights(f_target)
        self.data_path = y_des.copy()



        plot = False
        if plot is True:
            # plot the basis function activations
            import matplotlib.pyplot as plt
            plt.figure(2)
            #plt.subplot(411)
            psi_track = self.gen_psi(self.cs.rollout())
            plt.plot(psi_track)
            plt.title('basis functions')
            #plt.show()
           # pdb.set_trace()

            plt.figure(3)
            #plt.subplot(412)
            plt.plot(f_target[:,0])
            plt.plot(np.sum(psi_track * self.w[0], axis=1) * self.dt)
            plt.legend(['f_target', 'w*psi'])
            plt.title('DMP forcing function knee')
            plt.tight_layout()


            t_y, t_dy, t_ddy = self.rollout()
            plt.figure(4)
            #plt.subplot(311)
            plt.plot(y_des[0])
            plt.plot(t_y[:,0], label = self.n_bfs)
            plt.legend(loc='lower right')
            plt.legend(['target', 'tracked'])
            plt.show()
            #plt.title('hip plot')

            #plt.show()

        self.reset_state()
        return y_des

    def rollout(self, timesteps=None, **kwargs):
        """Generate a system trial, no feedback is incorporated."""

        self.reset_state()

        if timesteps is None:
            if 'tau' in kwargs:
                timesteps = int(self.timesteps / kwargs['tau'])
            else:
                timesteps = self.timesteps

        # set up tracking vectors
        y_track = np.zeros((timesteps, self.n_dmps))
        dy_track = np.zeros((timesteps, self.n_dmps))
        ddy_track = np.zeros((timesteps, self.n_dmps))

        # import scipy.interpolate
        # path = np.zeros((self.timesteps))
        # x = np.linspace(0, self.cs.run_time, self.external_force.shape[0]) #linear spacing start, end, number of steps

        # path_gen = scipy.interpolate.interp1d(x, self.external_force) # row by row path generation for each joint
        # for t in range(self.timesteps):
        #     path[t] = path_gen(t * self.dt)

        # self.external_force = path

        for t in range(timesteps):
            ext= self.external_force[t]
            # run and record timestep
            y_track[t], dy_track[t], ddy_track[t] = self.step(external_force= ext, c_a=1, c_v=1, **kwargs)


            #pdb.set_trace()
        # desired and tracked path
        plot = False
        if plot is True:
            import matplotlib.pyplot as plt
            plt.figure(4)
            plt.subplot(411)
            plt.plot(self.data_path[0])
            plt.plot(y_track[:,0])
            plt.legend(loc='lower right')
            plt.legend(['target', 'tracked'])
            plt.title('hip plot')

            # plot the desired forcing function vs approx
            plt.subplot(412)
            plt.plot(self.data_path[1])
            plt.plot(y_track[:,1])
            plt.legend(loc='lower right')
            plt.legend(['target', 'tracked'])
            #plt.legend(['%i BFs' % i for i in self.n_bfs], loc='lower right')
            plt.title('knee plot')
            plt.tight_layout()

            plt.subplot(413)
            plt.plot(self.data_path[2])
            plt.plot(y_track[:,2])
            plt.legend(loc='lower right')
            #plt.legend(['%i BFs' % i for i in self.n_bfs], loc='lower right')
            plt.legend(['target', 'tracked'])
            plt.title('ankle plot')
            plt.tight_layout()
        return y_track, dy_track, ddy_track

    def reset_state(self):
        """Reset the system state"""
        self.y = self.y0.copy()
        self.dy = np.zeros(self.n_dmps)
        self.ddy = np.zeros(self.n_dmps)
        self.cs.reset_state()

    #def step(self, tau=1.0, error=0.0, external_force=None):
    def ILC(self, interaction_force):
        Q = 0.99 # positive scalars
        L = 1 # positive scalars
        c = 0.5 # learning from present


        #ILC from LPV
        #temp_u=kp*self.th_e+ kd*(self.e[i+1]-self.e[i])
        #FC-i = Coupled Learned Force, current iteraton learning control
        e_i = -interaction_force
        e_dot = e_i -self.e_i
        self.e_i = e_i
        self.FC_i = Q*(self.FC_i+ L*c*e_dot)
        C_i = c*self.e_i+ self.FC_i
        return C_i

    def get_target(self, y_des, ext_force):
        # calculate velocity of y_des
        dy_des = np.diff(y_des) / self.dt
        # add zero to the beginning of every row
        dy_des = np.hstack((np.zeros((self.n_dmps, 1)), dy_des))

        # calculate acceleration of y_des
        ddy_des = np.diff(dy_des) / self.dt
        # add zero to the beginning of every row
        ddy_des = np.hstack((np.zeros((self.n_dmps, 1)), ddy_des))

        f_target = np.zeros((y_des.shape[1], self.n_dmps))
        # find the force required to move along this trajectory
        if ext_force is not None:
            for d in range(self.n_dmps):
                f_target[:, d] = (ddy_des[d] - self.ay[d] *
                                  (self.by[d] * (self.goal[d] - y_des[d]) -
                                  dy_des[d])-ext_force)
        else:
            for d in range(self.n_dmps):
                f_target[:, d] = (ddy_des[d] - self.ay[d] *
                                  (self.by[d] * (self.goal[d] - y_des[d]) -
                                  dy_des[d]))

        return f_target

    def weight_update(self, f_target, r):
        x_track = self.cs.rollout() # equation 2.5
        psi = self.gen_psi(x_track) # equation 2.7
        #print("kamina")
        #print(self.w.shape)
        weight = self.w_p
        #print("size of the f_target", f_target.shape)
        #print("size of the psi", psi.shape)
        error = self.error
        P = self.P

        for i in range (self.n_bfs):
            error[:,i] = f_target[:,0] - weight[:,i]*r
            #pdb.set_trace()
            #print(error[:,i])
            #P = np.linalg.inv(weight)
            lamb = 0.97 #forgetting factor
            upper= np.power(P[:,i], 2)*np.power(r,2)
            lower = (lamb/psi[:,i])+(P[:,i]*np.power(r,2))+ 1e-8 
            P[:,i] = 1/lamb*(P[:,i]-(upper/lower))
            #print("self weight")
            #print (self.w[0])
            #print(self.w[0].shape)
            # print(np.size(self.w[0],0))
            # print(np.size(self.w[0],1))
            #print("changed_weight")

            self.w_p[:,i] = self.w_p[:,i]+ (psi[:,i]*P[:,i]*r*error[:,i]) #628*1 628*1 628*1 628*1
        #print (w)
        #print(w.shape)
        #self.w_p[0] = np.array(w_p) 
        self.error = error
        self.P = P



        # updating current weights
        for i in range(self.n_bfs):
            self.w[0, i] = np.sum(self.w_p[:,i])


    def step(self, tau=1.0, error=0.0, external_force=None, c_v=0.0, c_a=0.0):
        """Run the DMP system for a single timestep.

        tau float: scales the timestep
                   increase tau to make the system execute faster
        error float: optional system feedback
        """

        error_coupling = 1.0 / (1.0 + error)
        # run canonical system
        x = self.cs.step(tau=tau, error_coupling=error_coupling)

        # generate basis function activation
        psi = self.gen_psi(x)

        for d in range(self.n_dmps):

            # generate the forcing term
            f = (self.gen_front_term(x, d) *
                 (np.dot(psi, self.w[d])) / np.sum(psi))#equation 2.6

            # DMP acceleration
            #self.ddy[d] = (self.ay[d] *
            #               (self.by[d] * (self.goal[d] - self.y[d]) -
             #              self.dy[d]/tau) + f) * tau
            ''' # old code
            self.ddy[d] = (self.ay[d] *
                           (self.by[d] * (self.goal[d] - self.y[d]) -
                           self.dy[d]) + f) /tau
            if external_force is not None:
                self.ddy[d] += external_force[d]
            self.dy[d] += self.ddy[d] * tau * self.dt * error_coupling
            self.y[d] += self.dy[d] * self.dt * error_coupling
            '''
            self.ddy[d] = (self.ay[d] *
                           (self.by[d] * (self.goal[d] - self.y[d]) -
                           self.dy[d]) + f) /tau
            if external_force is not None:
                C_i = self.ILC(external_force)
                #self.ddy[d] += c_a* external_force/ self.dt
                self.ddy[d] += c_a* C_i/ self.dt
            self.dy[d] += self.ddy[d] * tau * self.dt * error_coupling
            if external_force is not None:
                #self.dy[d] += c_v*external_force
                self.dy[d] += C_i
            self.y[d] += self.dy[d] * self.dt * error_coupling
            #pdb.set_trace()

            #print('the value of force', f)
        return self.y, self.dy, self.ddy #figure 7
