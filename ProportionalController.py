import numpy as np

class ProportionalController(object):
    def __init__(self, x0, kp):
        # Initialize controller state
        self.x = 0
        self.kp = kp

    def getOutput(self, ref, y):
        # u_k = kp*(r - y_k)
        # Controlling x-position
        ref_x = ref[0][0]
        y_x = y[0][0]
        return np.array([[self.kp*(ref_x - y_x)], [0]])

    def updateState(self, ref, y, dt):
        # x_k+1 = 0
        pass
