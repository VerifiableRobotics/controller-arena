# code for python reference dipole vector field controller

# these functions require stuff
#from mathFuns import *
from numpy import *
from math import *

class refVec:
	# define the constructor
    def __init__(self, q0, gain):
        # Initialize controller state
        pass

    def getVectorField(self, q, q_d):
		# return type: numpy array
		# note: unsure if this vector field was just an example from the paper!!
		# compute vector field F
		# unpack
		x = q[0][0]
		y = q[1][0]
		x_d = q_d[0][0]
		y_d = q_d[1][0]
		#
		# compute [taken from paper draft]
		Fx = 2*(x - x_d)**2 - (y - y_d)**2
		Fy = 3*(x - x_d)*(y - y_d)
		F = array([Fx,Fy])
		return F

    def getControl(self, q, q_d, F):
		# I think that this control law is not a function of the vector field, and that it should
		# work if F(q) changes
		# 
		# compute control signal u
		# unpack
		x = q[0][0]
		y = q[1][0]
		x_d = q_d[0][0]
		y_d = q_d[1][0]
		delta_p = array([ [x-x_d],[y-y_d] ]) #q - q_d # can I do this in python? # intended to be a 1x2 array
		theta = q[2][0]
		# set gains
		k_u = 0
		k_w = 0
		Fx = F[0]
		Fy = F[1]
		phi = atan2(Fy,Fx)
		phiDot = 1/(1+(Fy/Fx)**2) # derivative done by hand (sign convention ok?)
		v = -k_u*sign( dot(transpose(delta_p)[0], array([[cos(theta)],[sin(theta)]]) )[0] )*tanh(linalg.norm(delta_p)**2) 
		w = -k_w*(theta - phi) + phiDot  # omega
		u = array([[v], [w]])
		print u
		return u

    def getOutput(self, q_d, q): # obtain reference vector field value
        F = self.getVectorField(q, q_d) # F is an array containing Fx and FY
        ## obtain control signal as a fcn of reference vector field value
        u = self.getControl(q, q_d, F)
        return u

    def updateState(self, q_d, q, dt):
    	# x_k+1 = 0
    	pass




