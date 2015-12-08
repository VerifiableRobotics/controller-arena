#P Controller
# x = state vector
# u = input vector

import math
import numpy as np


class PController:
    def __init__(self, kp, controller_flag, dt): #call state and gain
        self.kp = kp #set gain
        self.stage = 0


    def getOutput(self, ref, y):

        # u_k = kp*(r - y_k)

        if self.stage == 0: #controller 1, rotate robot so that it faces destination point
            beta = math.atan2(ref[1][0],ref[0][0]) #angle from robots current orientation to face destionation
            y_th = y[2][0] #current orientaiton angle

            err = abs(beta - y_th)

            if err > 1e-3:
                return np.array([[0],[self.kp*(beta - y_th)]])

            else:
                self.stage += 1
                return np.array([[0],[0]])

        elif self.stage == 1: #controller 2, move robot along 1-D line of motion to arrive at dest point
            r = math.sqrt(y[0][0]**2 + y[1][0]**2) #distance from origin
            rd = math.sqrt(ref[0][0]**2 + ref[1][0]**2) #distance of end point from origin

            err = abs(r - rd)

            if err > 1e-3:
                return np.array([[self.kp*(rd - r)], [0]])
            else:
                self.stage += 1
                return np.array([[0],[0]])

        else: #controller 3, rotate robot so that it is oriented correctly now that it is at dest pt
            ref_th = ref[2][0] #angle from robots current orientation to face destionation
            y_th = y[2][0] #current orientaiton angle

            err = abs(ref_th - y_th)
            if err > 1e-3:
                return np.array([[0],[self.kp*(ref_th - y_th)]])
            else:
                return np.array([[0],[0]])
