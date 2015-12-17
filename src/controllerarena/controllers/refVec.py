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
        self.e_int_w = 0
        self.e_int_u = 0
        
        # set gains
        self.k_p_u = 1  # u indicates it is an position gain. p indicates it is a proportional gain.
        self.k_p_w = 3   # w indicates it is an angular gain. p indicates it is a proportional gain.
        if controller_flag == 1: # PID
            self.k_i_w = 1
            self.k_i_u = 1
            self.k_d = -1 # the derivative gain is only on the angle
        elif controller_flag == 2: # PI
            self.k_i_w = 1
            self.k_i_u = 1
            self.k_d = 0
        elif controller_flag == 3: # PD
            self.k_i_w = 0
            self.k_i_u = 0
            self.k_d = -1
        else: # P
            self.k_i_w = 0
            self.k_i_u = 0
            self.k_d = 0

    def get_output(self, q_d, q, dt): # obtain reference vector field value
        F = self.get_vector_field(q, q_d) # F is an column vector
        ## obtain control signal as a fcn of reference vector field value
        u = self.get_control(q, q_d, F, dt)
        return u

    def get_vector_field(self, q, q_d):
		# return type: numpy array
        lamb = 3
        theta_d = q_d[2][0]
        delta_p = q[0:2] - q_d[0:2] # location - location_desired
        r = array([[cos(theta_d)],[sin(theta_d)]]) 
        F = lamb*(dot(transpose(r), delta_p)[0][0])*delta_p - r*(dot(transpose(delta_p),  delta_p)[0][0]) # should be col vector
        #print F
        return F # col vector
    
    def get_control(self, q, q_d, F, dt):
		# I think that this control law is not a function of the vector field, and that it should
		# work if F(q) changes
		# 
		# compute control signal u 
        delta_p = q[0:2] - q_d[0:2] # location - location_desired
        self.e_int_w += self.sub_angles(q[2][0],q_d[2][0])*dt # accumulate angular error
        self.e_int_u += linalg.norm(delta_p)*dt # accumulate position error
        theta = q[2][0]
        
        # unpack gains
        k_p_u = self.k_p_u
        k_p_w = self.k_p_w
        k_i_w = self.k_i_w
        k_i_u = self.k_i_u
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
        v = -k_p_u*sign( dot(transpose(delta_p), array([[cos(theta)],[sin(theta)]]) )[0][0] )*tanh(linalg.norm(delta_p)**2) - k_i_u*self.e_int_u
        w = -k_p_w*self.sub_angles(theta, phi) - k_i_w*self.e_int_w - k_d*phi_dot  # k_d determines whether derivative term is used, k_i for i term
        u = array([[v], [w]])
        #print u
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



