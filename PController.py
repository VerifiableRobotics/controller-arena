#P Controller
# x = state vector
# u = input vector
from AbstractIOModel import *
import numpy as np

# Implementing abstract methods
class ProportionalController(AbstractIOModel):
    def __init__(self, x, dt): #call state and delta t 
        self.x = x #set state to x
        self.dt = dt #set time step to delta t
        
        #hard coding endpoint in for rn 
        
        self.ref = array([3, 4, math.pi/2]) #desired ending point of
        
        self.kp = 10 #gain 

    def step(self, u):
        
        #controller 1, rotate robot so that it faces destination point
        beta = math.arctan(self.ref[1]/self.ref[0]) #angle of dest point wrt Golobal
        del_theta = (beta - self.x[2]) #diff in angle betweeen bot and dest pt
        if del_theta <= .001: 
            err = self.ref[2] - u[2] #find angle difference from target location 
            u = self.kp*array([[0.],[err]]) #update u vector with omega to move
            del_theta = beta - (self.x[3] + u[1]*self.dt) #update del_theta with new angle diff 
        return u #output vector with velovity
        
        #controller 2, move robot along 1-D line of motion to arrive at dest point
        
        r = math.sqrt(self.x[0]^2 + self.x[1]^2) #distance from origin
        rd = math.sqrt(self.ref[0]^2 + self.ref[1]^2) #distance of end point from origin
        
    
        if (rd-r) <= 0.001:
            
            xerr[0] = self.ref[0] - math.cos(self.x[2])*u[0] #find x error
            yerr[0] = self.ref[1] - math.cos(self.x[2])*u[0] #find x error
            err = math.sqrt(xerr[0]^2 + yerr[1]^2) 
            u = self.kp*np.array([[err[0]], [0.]]) #update u vector with velocity to move 
        return u #output vector with velovity
    
    
       #controller 3, rotate robot so that it is oriented correctly now that it is at dest pt
       
        del_theta = (self.ref[2] - self.x[2]) #diff in angle betweeen bot and dest pt
        if del_theta <= .001: 
            err = self.ref[2] - u[2] #find angle diff from bot orientation and target orientation 
            u = self.kp*array([[0.],[err]]) #update u vector with omega to move
            del_theta = beta - (self.x[3] + u[1]*self.dt) #update del_theta with new angle diff 
        return u #output vector with velovity
        
    
