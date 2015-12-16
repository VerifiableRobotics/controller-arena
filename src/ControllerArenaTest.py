from controllerarena.ControllerArena import *
import controllerarena.controllers.PController as PC
import controllerarena.controllers.refVec as RV
import numpy as np
import json

# Time step
# dt = 0.05
dt = 0.032
# Stop tolerance
tol = 2e-1
# Reference vector
ref = np.array([[3], [2], [2]])
### ref = np.array([[-3], [4], [1.57]])
# Proportional gain
kp = 0.2
# Initial plant state
x0 = np.array([[0], [0], [0]])

ca = ControllerArena()

### configs = json.dumps({'config': [{'x': 1, 'y': 2, 'xlabel': 'x (m)', 'ylabel': 'y (m)'}, {'x': 0, 'y': 3, 'xlabel': 't (s)', 'ylabel': 'theta (rad)'}]})
configs = "Start"

ca.config(configs)

### ca.sim(PC.PController, kp, ref, x0, dt, tol, 1)
ca.sim(RV.refVec, x0, ref, x0, dt, tol, 3)
