import socket
import time
import UnicycleKinematic as UK
import ProportionalController as PC
import numpy as np
from math import pi

# Socket address
HOST = '127.0.0.1'
PORT = 8080
# Open socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to socket
s.connect((HOST, PORT))

# Time step
DT = 0.05
# Reference vector
ref = np.array([[10], [0], [0]])
# Initial controller state
x0_c = 0
# Proportional gain
kp = 2
# Initialize controller
pc = PC.ProportionalController(x0_c, kp)
# Initial plant state
x0_p = np.array([[0], [0], [0]])
# Initialize plant
uk = UK.UnicycleKinematic(x0_p)
# Initial plant output (controller input delayed 1 step to break algebraic loop)
y = np.array([[0], [0], [0]])

# Simulation
while abs(ref[0]-y[0] > 1e-6):
    # Controller current output
    u = pc.getOutput(ref, y)
    # Step controller forward
    pc.updateState(ref, y, DT)
    # Plant current output
    y = uk.getOutput(u)
    # Step plant forward
    uk.updateState(u, DT)
    # Log plant output
    s.sendall(str(y))
    # Delay by time step
    time.sleep(DT)
# Controller after final step
u = pc.getOutput(ref, y)
# Plant after final step
y = uk.getOutput(u)
# Log final plant output
s.sendall(str(y))

# Close connection
s.close()
