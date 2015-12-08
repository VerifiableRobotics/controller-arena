import socket
import json
import Metrics

def decode(dct):
    if "data" in dct:
        return dct["data"]
    else:
        return "Invalid JSON"

def process(datum):
    arr = json.loads(datum, object_hook=decode)
    return ','.join(map(lambda x: str(x), arr))

# Opening csv for logging
fid = open('log.csv', 'w')
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
conn.recv(1024)
conn.sendall('Ready')
while 1:
    # Receive data
    datum = conn.recv(1024)
    if datum:
        # If data is not terminating
        try:
            # Process and print data
            res = process(datum)
            print res
            fid.write(res + '\n')
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
# Close file
fid.close()

m = Metrics.Metrics()
print m.totalTime()
# print m.normalizedTime()
print m.chatter()
print m.oscillitory()
print m.OverShoot()
