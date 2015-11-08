# code for python reference dipole vector field controller

# these functions require stuff
#from mathFuns import *
from numpy import *
from math import *

class refVec:
	# define the constructor
    def __init__(self, q_0, r):
        # Initialize controller state
        self.r = r # column vector; parameter used to construct vector field
        self.phi_prev = q_0[3][0]
        pass

    def getVectorField(self, q, q_d):
		# return type: numpy array
		# note: unsure if this vector field was just an example from the paper!!
		# compute vector field F
		# unpack
		#x = q[0][0]
		#y = q[1][0]
		#x_d = q_d[0][0]
		#y_d = q_d[1][0]
		#
		# compute [taken from paper draft]
		#Fx = 2*(x - x_d)**2 - (y - y_d)**2
		#Fy = 3*(x - x_d)*(y - y_d)
		lamb = 3
		r = self.r
		F = lamb*(dot(transpose(r)[0], q)[0])*q - r*(dot(transpose(q)[0], q)[0]) # should be col vector
		return F

    def getControl(self, q, q_d, F, dt):
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
		k_u = 1
		k_w = 1
		Fx = F[0][0]
		Fy = F[1][0]
		phi = atan2(Fy,Fx)
		phiDot = 0 # just for now
		# backward finite difference for phidot
		phiDot = (phi-self.phi_prev)/dt
		# if we are not on the initial step, set phi_prev to the newly computed phi for the next loop
		self.phi_prev = phi
		v = -k_u*sign( dot(transpose(delta_p)[0], array([[cos(theta)],[sin(theta)]]) )[0] )*tanh(linalg.norm(delta_p)**2) 
		w = -k_w*modAngles(theta, phi) + phiDot  # omega
		u = array([[v], [w]])
		return u

    def getOutput(self, q_d, q): # obtain reference vector field value
        F = self.getVectorField(q, q_d) # F is an column vector
        ## obtain control signal as a fcn of reference vector field value
        u = self.getControl(q, q_d, F, dt)
        return u

    def updateState(self, q_d, q, dt):
    	# x_k+1 = 0
    	pass

    def modAngles(ang1, ang2):
    	return (ang1 - ang2 + pi)%(2*pi) - pi
# For future:
# pass r vector as parameter - done
# low pass filtering for derivatives (PD control?) [phidot]
# visual stuff
# global feedback plan is the ref vecf field
# controller is a function of vector field, but you can use a better controller to get better performance



