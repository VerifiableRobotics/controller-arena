import socket
import matplotlib.pyplot as plt
import numpy as np

# Time step
dt = 0.05
# Stop time
t_stop = 10

# Set up plot
plt.figure()
# Data line
l, = plt.plot([], [], 'r-')
# Set x-axis limits
plt.xlim(0, t_stop)
# Don't block when showing plot
plt.show(block=False)


def process(l, datum):
    # Extract x-coordinate
    datum = float(datum[2:-2].split(']\n [')[0].strip())
    # Get xy data from plot
    x = l.get_xdata()
    y = l.get_ydata()
    if len(x) > 0:
        # Append new data
        l.set_xdata(np.append(x, l.get_xdata()[-1]+dt))
        l.set_ydata(np.append(y, datum))
        # Adjust y-axis limits
        plt.ylim(0, np.amax(l.get_ydata())*1.05)
    else:
        # Add first coordinates
        l.set_xdata([0])
        l.set_ydata([datum])
    # Update plot
    plt.draw()

# Socket address
HOST = '127.0.0.1'
PORT = 8080
# Open socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to address
s.bind((HOST, PORT))
# Listen (1 connection in buffer)
s.listen(1)
# Accept connection
conn, addr = s.accept()
print "Connected by", addr
while 1:
    # Receive data
    datum = conn.recv(1024)
    if datum:
        # If data is not terminating
        try:
            # Process and plot data
            process(l, datum)
        except:
            # Handle invalid data without closing connection
            print "Invalid data received"
    else:
        # If data is terminating
        break
# Close connection
conn.close()
# Close socket
s.close()
# Keep showing plot
plt.show()
