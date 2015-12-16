import socket
import time
import numpy as np
import json

class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        return {'data': map(lambda x: x[0], obj)}

class ControllerArena(object):
    def __init__(self):
        # Socket address
        HOST = '127.0.0.1'
        PORT = 8080
        # Open socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to socket
        self.s.connect((HOST, PORT))

    def config(self, configs):
        # Send configuration string to Visual Logger server
        self.s.sendall(configs)
        self.s.recv(1024)
        print 'Logger configured'

    def sim(self, Controller, kp, ref, x0, dt, tol, controller_flag):
        # Initialize controller
        C = Controller(kp, controller_flag, dt)
        # Initialize plant
        HOST = '127.0.0.1'
        PORT = 8082
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        # Initialize output
        y = x0
        # Initialize time
        t = 0
        # Stop condition buffer
        buff = [y, y]
        # Simulation
        while not (abs(np.linalg.norm(buff[0]-ref)) < tol and abs(np.linalg.norm(buff[1]-ref)) < tol):
            # Get controller output
            u = C.getOutput(ref, y)
            # Get plant output
            s.sendall(str(u))
            y = s.recv(1024)
            y = np.array(map(lambda x: [x], map(lambda x: float(x.strip()[1:-1]), y[1:-1].split('\n'))))
            # Add time to output vector
            out = np.concatenate((np.array([[t]]), y, u, ref))
            # Log plant output
            out = json.dumps(out, cls=DataEncoder)
            self.s.sendall(out)
            # Update time
            t += dt
            # Delay time step
            time.sleep(dt)
            # Update buffer
            buff[1] = buff[0]
            buff[0] = y

    def __del__(self):
        # Close connection
        self.s.close()
