import socket

def process(datum):
    return ','.join(map(lambda x: x.strip(), datum[2:-2].split(']\n [')))

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
            # Process and print data
            print process(datum)
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
