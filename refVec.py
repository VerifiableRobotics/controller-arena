# code for python reference dipole vector field controller

# these functions require stuff
from mathFuns import *
from numpy import *
from math import *

""" this is the top level fucntion that will call all of the other functions. It will produce 
a control signal as the output """
def RVFcontroller(q, q_d):
	# obtain reference vector field value
	F = getVectorField(q, q_d) # F is an array containing Fx and FY
	#
	# obtain control signal as a fcn of reference vector field value
	u = getControl(q, q_d, F)
	return u

def getVectorField(q, q_d):
	# return type: numpy array
	# note: unsure if this vector field was just an example from the paper!!
	# compute vector field F
	# unpack
	x = q[0]
	y = q[1]
	x_d = q_d[0]
	y_d = q_d[1]
	#
	# compute [taken from paper draft]
	Fx = 2*(x - x_d)**2 - (y - y_d)**2
	Fy = 3*(x - x_d)*(y - y_d)
	F = array([Fx Fy])
	return F

def getControl(q, q_d, F):
	# I think that this control law is not a function of the vector field, and that it should
	# work if F(q) changes
	# 
	# compute control signal u
	# unpack
	delta_p = q - q_d # can I do this in python? # intended to be a 1x2 array
	theta = q[2]
	# set gains
	k_u = 1
	k_w = 1
	# following two lines aren't yet functional
	Fx = F[0]
	Fy = F[1]
	phi = atan2(Fy,Fx)
	phiDot = 1/(1+(Fy/Fx)^2) # derivative done by hand (sign convention ok?)
	v = -k_u*sign(delta_p*array([[cos(theta)],[sin(theta)]])*tanh(abs(delta_p)**2) 
	w =-k_w*(theta - phi) + phiDot  # omega
	u = array([v w])
	return u

	## figure out how to deal with arrays in python




