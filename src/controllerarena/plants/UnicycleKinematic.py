import numpy as np
from math import sin, cos

class UnicycleKinematic(object):
    def __init__(self, x0):
        # Initialize plant state
        self.x = np.copy(x0.astype(float))

    def getOutput(self, u, dt):
        # y_k = x_k
        y = np.copy(self.x)
        self.updateState(u, dt)
        return y

    def updateState(self, u, dt):
        # x_k+1 = x_k + B_k*u_k
        theta = self.x[2]
        B = np.matrix([[cos(theta), 0], [sin(theta), 0], [0, 1]])
        #print B
        #print u
        #print dt
        self.x += B*u*dt
