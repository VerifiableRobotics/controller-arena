from controllerarena.ControllerArena import *
import controllerarena.controllers.refVec as rv
import controllerarena.plants.UnicycleKinematic as UK
import numpy as np
import json


# Time step
dt = 0.05
# Stop tolerance
tol = 1e-1
# Reference vector
ref = np.array([[10], [10], [np.pi/2]])
# Proportional gain
kp = 9
# reference vector controller paramter
controller_flag = 3 # 1: PID, 2:PI, 3:PD, 4:P
# Initial plant state
x0 = np.array([[0], [0], [0]])

configs = json.dumps({'config': [{'x': 1, 'y': 2, 'xlabel': 'x (m)', 'ylabel': 'y (m)'}, {'x': 0, 'y': 3, 'xlabel': 't (s)', 'ylabel': 'theta (rad)'}]})

ca = ControllerArena()

# ca.config(configs)
ca.config("start")

ca.sim(rv.refVec, kp, UK.UnicycleKinematic, ref, x0, dt, tol, controller_flag)
