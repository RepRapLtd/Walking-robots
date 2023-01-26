import socket
import sys

#exec(open('server.py').read())

s = "Status register: 0x77 <br> Control register: 0x1f <br> Chip temperature: 24oC <br> V0: 1.5466 V <br> V1: 1.5466 V <br> V2: 1.5466 V <br> V3: 1.5466 V <br> Supply: 3.309 V"

HOST, PORT = "localhost", 9999
#data = " ".join(sys.argv[1:])
data = s

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print(format(received))




#print(s)


