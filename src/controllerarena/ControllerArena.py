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
        print 'Visual Logger configured'

    def sim(self, Controller, kp, Plant, ref, x0, dt, tol):
        # Initialize controller
        C = Controller(kp)
        # Initialize plant
        P = Plant(x0)
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
            y = P.getOutput(u, dt)
            # Add time to output vector
            out = np.concatenate((np.array([[t]]), y))
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
        #Get final controller output
        u = C.getOutput(ref, y)
        # Get final plant output
        y = P.getOutput(u, dt)
        # Add time to output vector
        out = np.concatenate((np.array([[t]]), y))
        # Log plant output
        out = json.dumps(out, cls=DataEncoder)
        self.s.sendall(out)

    def __del__(self):
        # Close connection
        self.s.close()
