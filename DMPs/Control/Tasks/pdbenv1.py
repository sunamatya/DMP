#!/usr/bin/env python
######################################
# This verison contains P + ILC control
###################################
import os
import errno
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
from pm_msgs.msg import PresStamped
import time
import numpy as np
import serial
import sys
import zmq
import capnp
import record_capnp
class Foo(object):
    """docstring for LocationMonitor"""
    def __init__(self):
        ##########################################
        #    Desired Position (mm)and Angle (deg)
        self.l_d=10
        self.th_d=10
        ###########################################
        # Initialization of two ceneter points
        self._x1=0.
        self._y1=0.
        self._z1=0.
        self._x2=0.
        self._y2=0.
        self._z2=0.
        #############################################
        # Initialization of ILC 
        self.num_iter=20
        self.num_index=1000 +101
        self.index=0
        self.iter=0
        self.e=np.array([0.0]*self.num_index)
        self.uk=np.array([0.0]*self.num_index)
        self.uk1=np.array([0.0]*self.num_index)
        self.x=np.array([0.0]*self.num_index)
        self.dx=np.array([0.0]*self.num_index)
        #############################################
        self.u=0. ### p+ilc
        self.l0=0
        self.l0s=0
        self.ths=0.
        self.l_e=0.
        self.l_esum=0.
        self.u_old=0.
        self.theta0=0.
        self.th_e=0.
        self.th_esum=0.
        self.u_th=0.
        self.u_thold=0.
        self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=115200)

        context = zmq.Context()
        self.socket2 = context.socket(zmq.PUB)
        self.socket2.setsockopt(zmq.CONFLATE,1)
        self.socket2.bind("tcp://10.203.49.10:1000")
        raw_input("Press Enter to Conti")
        # pub=rospy.Publisher("/LV/PD",String,queue_size=1)
        rospy.Subscriber("/Robot_1/pose",PoseStamped,self.rbody1,queue_size=1)
        # rospy.Subscriber("/Robot_2/pose",PoseStamped,self.rbody3)
        rospy.Subscriber("/Robot_2/pose",PoseStamped,self.rbody2,queue_size=1)
        # pub.publish(String(self.u))
        rospy.spin()

    # def cal_angle(v1,v2, acute):
    # # v1 is your firsr vector
    # # v2 is your second vector
    #     angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    #     if (acute == True):
    #         return angle
    #     else:
    #         return 2 * np.pi - angle
    def rbody3(self,msg_pos2):

        self._x22 =msg_pos2.pose.position.x
        self._y22 =msg_pos2.pose.position.y
        self._z22 =msg_pos2.pose.position.z

    def rbody1(self,msg_pos1):
        self._x1 =msg_pos1.pose.position.x
        self._y1 =msg_pos1.pose.position.y
        self._z1 =msg_pos1.pose.position.z
        ini_x=np.array([0.001,0,0])
        ini_y=np.array([0,0.001,0])
        ini_z=np.array([0,0,0.001])

        vec = np.array([self._x1-self._x2,self._y1-self._y2,self._z1-self._z2])
        l=np.sqrt(vec.dot(vec))
        theta_x=180*(np.arccos(np.dot(ini_x, vec) / (np.linalg.norm(ini_x) * np.linalg.norm(vec))))/np.pi
        theta_y=180*(np.arccos(np.dot(ini_y, vec) / (np.linalg.norm(ini_y) * np.linalg.norm(vec))))/np.pi
        theta_z=180*(np.arccos(np.dot(ini_z, vec) / (np.linalg.norm(ini_z) * np.linalg.norm(vec))))/np.pi
        theta_z=theta_y
        msg1=record_capnp.Message.new_message()
        msg1.x1=self._x1
        msg1.y1=self._y1
        msg1.z1=self._z1
        msg1.x2=self._x2
        msg1.y2=self._y2
        msg1.z2=self._z2
        msg1.theta=round(self.th_d-(theta_z-self.ths),4)
        msg1.le=round(self.l_d-(l-self.l0s)*1000.,4)
        en_msg1=msg1.to_bytes()
        self.socket2.send(en_msg1)
        # print 1
    def rbody2(self,msg_pos2):
        ########################
        # PID Gains for Feedback
        kp=3
        kd=.01
        kd=0
        # kpl=2
        ts=100
        temp_u=0.
        # kp_th=1.
        # ki_th=0.
        # kd_th=0.
        # temp_uth=0.
        #######################

        self._x2 =msg_pos2.pose.position.x
        self._y2 =msg_pos2.pose.position.y
        self._z2 =msg_pos2.pose.position.z
        vec = np.array([self._x1-self._x2,self._y1-self._y2,self._z1-self._z2])
        ini_x=np.array([0.001,0,0])
        ini_y=np.array([0,0.001,0])
        ini_z=np.array([0,0,0.001])
        l=np.sqrt(vec.dot(vec))
        theta_x=180*(np.arccos(np.dot(ini_x, vec) / (np.linalg.norm(ini_x) * np.linalg.norm(vec))))/np.pi
        theta_y=180*(np.arccos(np.dot(ini_y, vec) / (np.linalg.norm(ini_y) * np.linalg.norm(vec))))/np.pi
        theta_z=180*(np.arccos(np.dot(ini_z, vec) / (np.linalg.norm(ini_z) * np.linalg.norm(vec))))/np.pi
        theta_z=theta_y
        # print theta_x,theta_y,theta_z
        if self.index <=99:
            self.l0=self.l0+l
            self.index=self.index+1
            self.theta0=self.theta0+theta_z
        elif self.index == 100:
            self.l0=self.l0/100.
            self.l0s=self.l0
            self.theta0=self.theta0/100.
            self.ths=self.theta0
            self.index=self.index+1
        elif self.index < self.num_index-1:
            i=self.index-101
            self.th_e=round(self.th_d-(theta_z-self.theta0),4)
            self.e[i+1]=self.th_e
            # self.th_e=round(self.th_d-(theta-self.theta0)*1000.,4)
            temp_u=kp*self.th_e+ kd*(self.e[i+1]-self.e[i])
            # self.uk1[i]=self.uk[i] +kpl*self.e[i+1]
            # temp_uth=kp_th*self.th_e+ ki_th*self.th_esum
            if temp_u> 25:
                self.u=25*100
                self.u_old=self.u
            elif temp_u<=0:
                self.u=self.u_old
            else:
                self.u=round(temp_u,2)*100
                self.u_old=self.u
            # sock.sendall(self.u)
            ser_msg=str(int(self.u)).zfill(4)
            # print len(ser_msg.encode('utf-8'))
            # self.ser.write(str(int(self.u)).zfill(4))
            # msg1=record_capnp.Message.new_message()
            # msg1.x1=self._x1
            # msg1.y1=self._y1
            # msg1.z1=self._z1
            # msg1.x2=self._x2
            # msg1.y2=self._y2
            # msg1.z2=self._z2
            # msg1.le=self.l_e
            # en_msg1=msg1.to_bytes()
            # self.socket2.send(en_msg1)
            print "Loop:",self.iter,"index",self.index-101,"Pd:",str(float(ser_msg)/100),"psi","Angle Error",str(round(self.th_e,2)),"deg"
            # time.sleep(0.02)
            self.index=self.index+1

        elif self.index ==self.num_index-1:
            self.u=0.
            # ser_msg=str(int(self.u)).zfill(4)
            self.ser.write(str(int(self.u)).zfill(4))
            self.iter=self.iter+1
            print "Loop:",self.iter,"is Done"
            # if self.iter > self.num_iter:
            raw_input("Press Enter to Conti.")
            self.index=101
            # self.l0=0

if __name__ == '__main__':
    try:
        rospy.init_node('LVPressure_ctl')
        # pub=rospy.Publisher("/LV/PD",String,queue_size=1)
        foo =Foo()
    except rospy.ROSInterruptException:
        foo.ser.close()



