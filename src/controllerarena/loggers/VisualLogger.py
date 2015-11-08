import socket
import matplotlib.pyplot as plt
import numpy as np
import json

idx = 0
lines = []

def decode(dct):
    if "data" in dct:
        return dct["data"]
    elif "config" in dct:
        return dct["config"]
    elif "config" not in dct and "x" in dct and "y" in dct:
        global idx, lines
        idx += 1
        plt.figure(idx)
        if "xlabel" in dct:
            plt.xlabel(dct["xlabel"])
        if "ylabel" in dct:
            plt.ylabel(dct["ylabel"])
        l, = plt.plot([], [], 'r-')
        lines.append(l)
        return [dct["x"], dct["y"]]
    else:
        return "Invalid JSON"

def process(lines, datum, configs):
    arr = json.loads(datum, object_hook=decode)
    for idx, config in enumerate(configs):
        plt.figure(idx+1)
        xdata = arr[config[0]]
        ydata = arr[config[1]]
        l = lines[idx]
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
configs = conn.recv(1024)
configs = json.loads(configs, object_hook=decode)
plt.show(block=False)
conn.sendall('Ready')
while 1:
    # Receive data
    datum = conn.recv(1024)
    if datum:
        # If data is not terminating
        try:
            # Process and plot data
            process(lines, datum, configs)
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
