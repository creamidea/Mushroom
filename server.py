# Echo server program
import socket
import sys
import signal

HOST = None               # Symbolic name meaning all available interfaces
PORT = 9001              # Arbitrary non-privileged port
s = None

for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print 'could not open socket'
    sys.exit(1)
conn, addr = s.accept()
print 'Connected by', addr

running = True
def signal_handler(signal, frame):
    print 'Your press Ctrl+C!'
    running = False
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

while True:
    data = conn.recv(1024)
    if not data: break
    conn.send(data)
    if not running:
        conn.close()
        break
