# code for python reference dipole vector field controller

# these functions require stuff
from mathFuns import *
import numpy np
import math

""" this is the top level fucntion that will call all of the other functions. It will produce 
a control signal as the output """
def RVFcontroller(q, q_d):
	# obtain reference vector field value
	[Fx, Fy] = getVectorField(q) 
	#
	# obtain control signal as a fcn of reference vector field value
	u = getControl(q, q_d, Fx, Fy)
	return u

def getVectorField(q, q_d):
	# compute vector field F
	# unpack
	x = q(0)
	y = q(1)
	x_d = q_d(0)
	y_d = q_d(1)
	#
	# compute [taken from paper draft]
	Fx = 2*(x - x_d)**2 - (y - y_d)**2
	Fy = 3*(x - x_d)*(y - y_d)
	#
	return [Fx Fy]

def getControl(q, q_d, Fx, Fy):
	# compute control signal u
	# unpack
	delta_p = q - q_d
	theta = q(2)
	# set gains
	k_u = 1
	k_w = 1
	# define delta p
	v = -k_u*sign()*np.tanh()
	w =-k_w*(theta - phi) + phiDot  # omega
	u = [v w]
	return u

	## figure out how to deal with arrays in python




