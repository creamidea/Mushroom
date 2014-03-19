import socket
import sys

HOST, PORT = "localhost", 9001
# data = " ".join(sys.argv[1:])
data = "Testing..."

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

counter = 0
# while True:
#     try:
#         # Connect to server and send data
#         sock.connect((HOST, PORT))
#         sock.sendall(data + "\n")
#         counter = counter + 1
#         # Receive data from the server and shut down
#         received = sock.recv(1024)
#         print "Received: {}".format(received)
#     except Exception:
        
#     finally:
#         print "Sent:     {}".format(data)
#         if counter > 4:
#             sock.close()
#             break

try:
    sock.connect((HOST, PORT))
    sock.sendall(data + "\n")
    counter = counter + 1
    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()
print "Sent:     {}".format(data)
print "Received: {}".format(received)

