from ControllerArena import *
import PController as PC
import UnicycleKinematic as UK
import numpy as np

# Time step
dt = 0.05
# Stop time
t_stop = 10
# Reference vector
ref = np.array([[10], [7], [2]])
# Initial controller state
x0_c = 0
# Proportional gain
kp = 9
# Initial plant state
x0_p = np.array([[0], [0], [0]])
# Initial plant output (controller input delayed 1 step to break algebraic loop)
y0 = np.array([[0], [0], [0]])

ca = ControllerArena()
ca.sim(PC.PController, kp, UK.UnicycleKinematic, ref, x0_c, x0_p, y0, dt, t_stop)
