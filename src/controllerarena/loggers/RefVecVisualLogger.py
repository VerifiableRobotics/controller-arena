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
        if "xd" in dct:
            # generate points for vector field
            xd = dct["xd"] #desired position x
            yd = dct["yd"] #desired position y
            xi = dct["xi"] #initial position x
            yi = dct["yi"] #initial position y
            thetaD = dct["theta"] #desired orientation
            L=3 # hardcoded vector field lambda for now
            n=20 #int(np.linalg.norm(np.array([[xi-xd],[yi-yd]])))+1 # hardcoded spacing of vector field for now
            X = np.mgrid[yd+n:yi:(2*n+1)*1j, xi:xd+n:(2*n+1)*1j][1]
            Y = np.mgrid[yd+n:yi:(2*n+1)*1j, xi:xd+n:(2*n+1)*1j][0]
            #
            # compute vector field
            U = np.zeros(shape=(2*n+1,2*n+1)) # initialize memory
            V = np.zeros(shape=(2*n+1,2*n+1)) # initialize memory
            r=np.array([[np.cos(thetaD)],[np.sin(thetaD)]])
            for i in xrange(0,2*n+1):
                for j in xrange(0,2*n+1):
                    p=np.array([[ X[i][j]-xd ],[ Y[i][j]-yd ]])
                    F = L*(np.dot(np.transpose(r), p)[0][0])*p - r*(np.dot(np.transpose(p),  p)[0][0])
                    F = (F/np.linalg.norm(F)) # this would normalize vector field so all arrows are the same length
                    U[i][j]=F[0][0]
                    V[i][j]=F[1][0]
            #
            # plot vector field
            plt.quiver(X,Y,U,V)
            
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
            plt.xlim(np.amin(l.get_xdata()), np.amax(l.get_xdata())+20)
            plt.ylim(np.amin(l.get_xdata()), np.amax(l.get_ydata())+20)
            # for visible portion of graph, calculate vector field
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
        
    # plot vector field
    
    
# Close connection
conn.close()
# Close socket
s.close()
# Keep showing plot
plt.show()
