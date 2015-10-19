import socket
import time

class ControllerArena:
    def __init__(self):
        # Socket address
        HOST = '127.0.0.1'
        PORT = 8080
        # Open socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to socket
        self.s.connect((HOST, PORT))

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
            # Log plant output
            self.s.sendall(str(y))
            # Update time
            t += dt
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
