from ControllerArena import *
import ProportionalController as PC
import UnicycleKinematic as UK
import numpy as np

# Time step
dt = 0.05
# Stop time
t_stop = 10
# Reference vector
ref = np.array([[10], [0], [0]])
# Initial controller state
x0_c = 0
# Proportional gain
kp = 1
# Initial plant state
x0_p = np.array([[0], [0], [np.pi/4]])
# Initial plant output (controller input delayed 1 step to break algebraic loop)
y0 = np.array([[0], [0], [np.pi/4]])

ca = ControllerArena()
ca.vis_config('1,2')
ca.sim(PC.ProportionalController, kp, UK.UnicycleKinematic, ref, x0_c, x0_p, y0, dt, t_stop)
