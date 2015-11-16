# code for python reference dipole vector field controller

# these functions require stuff
#from mathFuns import *
from numpy import *
from math import *

class refVec:
	# define the constructor
    def __init__(self, q_0, controller_flag):
        # Initialize controller state
        self.phi_prev = None
        self.q_prev = q_0
        self.e_int = 0
        
        # set gains
        self.k_u = 1
        self.k_w = 1
        if controller_flag == 1: # PID
            self.k_i = 1
            self.k_d = 1
        elif controller_flag == 2: # PI
            self.k_i = 1
            self.k_d = 0
        elif controller_flag == 3: # PD
            self.k_i = 0
            self.k_d = 1
        else: # P
            self.k_i = 0
            self.k_d = 0


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
        #		x = q[0][0]
        #		y = q[1][0]
        #		x_d = q_d[0][0]
        #		y_d = q_d[1][0]
        #		#
        #		# compute [taken from paper draft], where r = [1;0] and lambda = 3
        #		Fx = 2*(x - x_d)**2 - (y - y_d)**2
        #		Fy = 3*(x - x_d)*(y - y_d)
        #		F = array([[Fx],[Fy]])
        lamb = 3
        theta_d = q_d[2][0]
        delta_p = q[0:2] - q_d[0:2] # location - location_desired
        r = array([[cos(theta_d)],[sin(theta_d)]]) 
        F = lamb*(dot(transpose(r), delta_p)[0][0])*delta_p - r*(dot(transpose(delta_p),  delta_p)[0][0]) # should be col vector
                 
        return F # col vector
    
    def get_control(self, q, q_d, F, dt):
		# I think that this control law is not a function of the vector field, and that it should
		# work if F(q) changes
		# 
		# compute control signal u 
        delta_p = q[0:2] - q_d[0:2] # location - location_desired
        self.e_int += self.sub_angles(q[2][0],q_d[2][0])*dt # accumulate angular error
        theta = q[2][0]
        
        # unpack gains
        k_u = self.k_u
        k_w = self.k_w
        k_i = self.k_i
        k_d = self.k_d
        
        Fx = F[0][0]
        Fy = F[1][0]
        phi = atan2(Fy,Fx)
        
		# backward finite difference for phidot
        if self.phi_prev == None: # if this is the first pass through the controller, phi_dot = 0
            self.phi_prev = phi
		# end if	
        phi_dot = (phi-self.phi_prev)/dt
        self.phi_prev = phi

        q_dot = (q-self.q_prev)/dt
        self.q_prev = q
        
        # controller
        v = -k_u*sign( dot(transpose(delta_p), array([[cos(theta)],[sin(theta)]]) )[0][0] )*tanh(linalg.norm(delta_p)**2) 
        w = -k_w*self.sub_angles(theta, phi) + k_i*self.e_int + k_d*phi_dot  # k_d determines whether derivative term is used, k_i for i term
        u = array([[v], [w]])

        return u

    def update_state(self, q_d, q, dt):
    	# x_k+1 = 0
    	pass

    def sub_angles(self, ang1, ang2):
    	return (ang1 - ang2 + pi)%(2*pi) - pi
# For future:
# pass r vector as parameter 
# low pass filtering for derivatives (PD control?) [phidot]
# visual stuff
# global feedback plan is the ref vecf field
# controller is a function of vector field, but you can use a better controller to get better performance



