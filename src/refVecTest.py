from controllerarena.ControllerArena import *
import controllerarena.controllers.refVec as rv
import controllerarena.plants.UnicycleKinematic as UK
import numpy as np
import json


# Time step
dt = 0.0005
# Stop tolerance
tol = .15
# Reference vector
xd=10
yd=10
thetaD=np.pi/2
ref = np.array([[xd], [yd], [thetaD]])
# Proportional gain
kp = 9
# reference vector controller paramter
controller_flag = 3 # 1: PID, 2:PI, 3:PD, 4:P
# Initial plant state
xi=0
yi=0
x0 = np.array([[xi], [yi], [0]])

configs = json.dumps({'config': [{'x': 1, 'y': 2,'xd': xd, 'yd': yd,'theta': thetaD,'xi': xi,'yi': yi, 'xlabel': 'x (m)', 'ylabel': 'y (m)'}, {'x': 0, 'y': 3, 'xlabel': 't (s)', 'ylabel': 'theta (rad)'}]})

ca = ControllerArena()

# ca.config(configs)
ca.config(configs)

ca.sim(rv.refVec, kp, UK.UnicycleKinematic, ref, x0, dt, tol, controller_flag)
