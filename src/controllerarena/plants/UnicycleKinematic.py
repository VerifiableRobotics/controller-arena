import numpy as np
from math import sin, cos
import socket

class UnicycleKinematic(object):
    def __init__(self, PORT, x0, dt):
        # Socket address
        HOST = '127.0.0.1'
        # Open socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind socket to address
        self.s.bind((HOST, PORT))
        # Listen (1 connection in buffer)
        self.s.listen(1)
        # Accept connection
        self.conn, addr = self.s.accept()
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

uk = UnicycleKinematic(8081, np.array([[0], [0], [0]]), 0.05)
while 1:
    control = uk.conn.recv(1024)
    if control:
        u = np.array(map(lambda x: [x], map(lambda x: float(x.strip()[1:-1]), control[1:-1].split('\n'))))
        y = uk.getOutput(u, 0.05)
        uk.conn.sendall(str(y))
    else:
        break
uk.s.close()
