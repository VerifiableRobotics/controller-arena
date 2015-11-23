# from ControllerArena import *
# import PController as PC
# import UnicycleKinematic as UK
from controllerarena.ControllerArena import *
import controllerarena.controllers.PController as PC
import controllerarena.plants.UnicycleKinematic as UK
import numpy as np
import json

# Time step
dt = 0.05
# Stop tolerance
tol = 1e-3
# Reference vector
ref = np.array([[10], [7], [2]])
# Proportional gain
kp = 8
# Initial plant state
x0 = np.array([[0], [0], [0]])

# configs = json.dumps({'config': [{'x': 1, 'y': 2, 'xlabel': 'x (m)', 'ylabel': 'y (m)'}, {'x': 0, 'y': 3, 'xlabel': 't (s)', 'ylabel': 'theta (rad)'}]})

ca = ControllerArena()
# ca.config(configs)
ca.config("Start")
# ca.sim(PC.ProportionalController, kp, UK.UnicycleKinematic, ref, x0_c, x0_p, y0, dt, t_stop)
ca.sim(PC.PController, kp, UK.UnicycleKinematic, ref, x0, dt, tol)
