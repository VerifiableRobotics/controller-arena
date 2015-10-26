#P Controller
# x = state vector
# u = input vector

import math
import numpy as np


class ProportionalController:
    def __init__(self, x0, kp): #call state and gain
        self.x = x #set state to x
        self.kp = kp #set gain 
        

    def getOutput(self, ref, y):
        
        # u_k = kp*(r - y_k)
        
        #controller 1, rotate robot so that it faces destination point
    
        beta = math.arctan(ref[1][0]/ref[0][0]) #angle from robots current orientation to face destionation 
        y_th = y[2][0] #current orientaiton angle 
        
        err = (beta - y_th)
        if err > 1e-6:
            return np.array([[0],[self.kp*(beta - y_th)]])
        
        #controller 2, move robot along 1-D line of motion to arrive at dest point
        r = math.sqrt(self.x[0]^2 + self.x[1]^2) #distance from origin
        rd = math.sqrt(self.ref[0]^2 + self.ref[1]^2) #distance of end point from origin
        
        err = (r -rd)
        
        if err < 1e-6:
            return np.array([[self.kp*(r - rd)], [0]])
        
        #controller 3, rotate robot so that it is oriented correctly now that it is at dest pt
        ref_th = ref[2][0] #angle from robots current orientation to face destionation 
        y_th = y[1][0] #current orientaiton angle 
        
        err = (ref_th - y_th)
        
        if err < 1e-6:
            return np.array([[0],[self.kp*(ref_th - y_th)]])
    
    def updateState(self, ref, y, dt):
        # theta_k+1 = 0
        pass    
        
        
        
     

    

    
       
        
    