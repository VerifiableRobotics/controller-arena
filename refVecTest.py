from ControllerArena import *
# import ProportionalController as PC
import refVec as rv
import UnicycleKinematic as UK
import numpy as np
import json

# Time step
dt = 0.05
# Stop time
t_stop = 10
# Reference vector
ref = np.array([[10], [10], [2]])
# Initial controller state
x0_c = 0
# Proportional gain
kp = 9
# reference vector field paramter
r = np.array([[1],[0]])
# reference vector controller paramter
controller_flag = 1 # 1: P"D", 3:P, 4:PI
# Initial plant state 
x0_p = np.array([[5], [5], [0]])
# Initial plant output (controller input delayed 1 step to break algebraic loop)
y0 = np.array([[5], [5], [0]])

configs = json.dumps({'config': [{'x': 1, 'y': 2, 'xlabel': 'x (m)', 'ylabel': 'y (m)'}, {'x': 0, 'y': 3, 'xlabel': 't (s)', 'ylabel': 'theta (rad)'}]})

ca = ControllerArena()

ca.config(configs)
# ca.sim(PC.ProportionalController, kp, UK.UnicycleKinematic, ref, x0_c, x0_p, y0, dt, t_stop)

ca.sim(rv.refVec, kp, r, UK.UnicycleKinematic, ref, x0_c, x0_p, y0, dt, t_stop, controller_flag)