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


def process(l, datum, config_arr):
    # Extract coordinates
    datum_arr = map(lambda (x): float(x.strip()), datum[2:-2].split(']\n ['))
    xdata = datum_arr[config_arr[0]]
    ydata = datum_arr[config_arr[1]]
    # Get xy data from plot
    x = l.get_xdata()
    y = l.get_ydata()
    if len(x) > 0:
        # Append new data
        l.set_xdata(np.append(x, xdata))
        l.set_ydata(np.append(y, ydata))
        # Adjust axis limits
        plt.xlim(0, np.amax(l.get_xdata())*1.05)
        plt.ylim(0, np.amax(l.get_ydata())*1.05)
    else:
        # Add first coordinates
        l.set_xdata([xdata])
        l.set_ydata([ydata])
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
config_str = conn.recv(1024)
config_arr = map(lambda (x): int(x), config_str.split(','))
conn.sendall('Ready')
while 1:
    # Receive data
    datum = conn.recv(1024)
    if datum:
        # If data is not terminating
        try:
            # Process and plot data
            process(l, datum, config_arr)
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
