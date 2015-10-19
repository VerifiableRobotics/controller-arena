import numpy as np
from math import sin, cos

class UnicycleKinematic:
    def __init__(self, x0):
        # Initialize plant state
        self.x = np.copy(x0.astype(float))

    def getOutput(self, u):
        # y_k = x_k
        return np.copy(self.x)

    def updateState(self, u, dt):
        # x_k+1 = x_k + B_k*u_k
        theta = self.x[2]
        B = np.matrix([[cos(theta), 0], [sin(theta), 0], [0, 1]])
        self.x += B*u*dt
