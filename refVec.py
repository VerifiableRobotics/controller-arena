# code for python reference dipole vector field controller

# these functions require stuff
#from mathFuns import *
from numpy import *
from math import *

class refVec:
	# define the constructor
    def __init__(self, q_0, r, controller_flag):
        # Initialize controller state
        # in the future, should r be a function of q_d ? 
        self.r = r # column vector; parameter used to construct vector field [dipole of dipole reference vector field]
        self.phi_prev = None
        self.q_prev = q_0
        self.controller_flag = controller_flag


    def get_output(self, q_d, q, dt): # obtain reference vector field value
        F = self.get_vector_field(q, q_d) # F is an column vector
        ## obtain control signal as a fcn of reference vector field value
        u = self.get_control(q, q_d, F, dt)
        return u

    def get_vector_field(self, q, q_d):
		# return type: numpy array
		# note: unsure if this vector field was just an example from the paper!!
		# compute vector field F
		# unpack
		x = q[0][0]
		y = q[1][0]
		x_d = q_d[0][0]
		y_d = q_d[1][0]
		#
		# compute [taken from paper draft], where r = [1;0] and lambda = 3
		Fx = 2*(x - x_d)**2 - (y - y_d)**2
		Fy = 3*(x - x_d)*(y - y_d)
		F = array([[Fx],[Fy]])
		#lamb = 3
		#r = self.r
		#F = lamb*(dot(transpose(self.r)[0], q)[0])*q - self.r*(dot(transpose(q)[0], q)[0]) # should be col vector
		return F # col vector

    def get_control(self, q, q_d, F, dt):
		# I think that this control law is not a function of the vector field, and that it should
		# work if F(q) changes
		# 
		# compute control signal u 
        delta_p = q[0:2][0] - q_d[0:2][0] # location - location_desired
		# set gains
        k_u = 1
        k_w = 1
        Fx = F[0][0]
        Fy = F[1][0]
        phi = atan2(Fy,Fx)
		# backward finite difference for phidot
        if self.phi_prev == None: # if this is the first pass through the controller, phi_dot = 0
            self.phi_prev = phi
		# end if	
        phi_dot = (phi-self.phi_prev)/dt
        self.phi_prev = phi

        vec_ang = array([[phi],[phi_dot]]) # vector field values. Store for passing
        q_dot = (q-self.q_prev)/dt
        self.q_prev = q
        
        if self.controller_flag == 1:
            u = self.original_control(q, delta_p, vec_ang, k_u, k_w)
        elif self.controller_flag == 2:
            u = self.more_D_PD_control(q, q_dot, delta_p, vec_ang, k_u, k_w)
        elif self.controller_flag == 3:
            u = self.P_control(q, delta_p, vec_ang, k_u, k_w)
        elif self.controller_flag == 4:
            u = self.PI_control(q, q_dot, delta_p, vec_ang, k_u, k_w)

        return u

# implement q_dot
# implement integral accumulator
# make sure var names and passing is compatible^

    def original_control(self, q, delta_p, vec_ang, k_u, k_w):
        phi = vec_ang[0][0]
        phi_dot = vec_ang[1][0]
        theta = q[2][0]
        v = -k_u*sign( dot(transpose(delta_p)[0], array([[cos(theta)],[sin(theta)]]) )[0] )[0]*tanh(linalg.norm(delta_p)**2) 
        w = -k_w*self.sub_angles(theta, phi) + phi_dot  # omega
        return array([[v], [w]]) # u
    
    def more_D_PD_control(self, q, q_dot, delta_p, vec_ang, k_u, k_w):
		pass
    
    def P_control(self, q, delta_p, vec_ang, k_u, k_w):
        phi = vec_ang[0][0]
        theta = q[2][0]
        v = -k_u*sign( dot(transpose(delta_p)[0], array([[cos(theta)],[sin(theta)]]) )[0] )[0]*tanh(linalg.norm(delta_p)**2) 
        w = -k_w*self.sub_angles(theta, phi) # angle minus angle desired at the current moment, which is phi
        return array([[v], [w]]) # u

    def PI_control(self, q, q_dot, delta_p, vec_ang, k_u, k_w):
		pass

    def update_state(self, q_d, q, dt):
    	# x_k+1 = 0
    	pass

    def sub_angles(self, ang1, ang2):
    	return (ang1 - ang2 + pi)%(2*pi) - pi
# For future:
# pass r vector as parameter - done
# low pass filtering for derivatives (PD control?) [phidot]
# visual stuff
# global feedback plan is the ref vecf field
# controller is a function of vector field, but you can use a better controller to get better performance



