import socket
import time
import numpy as np

class ControllerArena(object):
    def __init__(self):
        # Socket address
        HOST = '127.0.0.1'
        PORT = 8080
        # Open socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to socket
        self.s.connect((HOST, PORT))

    def vis_config(self, config_str):
        # Send configuration string to Visual Logger server
        self.s.sendall(config_str)
        self.s.recv(1024)
        print 'Visual Logger configured'

    def sim(self, Controller, kp, Plant, ref, x0_c, x0_p, y0, dt, t_stop):
        # Initialize controller
        C = Controller(x0_c, kp)
        # Initialize plant
        P = Plant(x0_p)
        # Initialize output
        y = y0
        # Initialize time
        t = 0
        # Simulation
        while t < t_stop:
            # Get controller output
            u = C.getOutput(ref, y)
            # Update controller state
            C.updateState(ref, y, dt)
            # Get plant output
            y = P.getOutput(u)
            # Update controller output
            P.updateState(u, dt)
            # Update time
            t += dt
            # Add time to output vector
            out = np.concatenate((np.array([[t]]), y))
            # Log plant output
            self.s.sendall(str(out))
            # Delay time step
            time.sleep(dt)
        # Get final controller output
        u = C.getOutput(ref, y)
        # Get final plant output
        y = P.getOutput(u)
        # Log plant output
        self.s.sendall(str(y))

    def __del__(self):
        # Close connection
        self.s.close()
