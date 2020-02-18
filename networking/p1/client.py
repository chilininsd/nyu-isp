import sys
from socket import *

if len(sys.argv) != 4:
    raise Exception("Not the right amount of args.\nUsage: client.py server_host server_port filename")

if not str.isdigit(sys.argv[2]):
    raise Exception("Port is not a number.\nUsage: client.py server_host server_port filename")

if not sys.argv[3]:
    raise Exception("No file name provided.\nUsage: client.py server_host server_port filename")

s = socket(AF_INET, SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))
host = "{}:{}".format(sys.argv[1], sys.argv[2])
try:
    req = "GET /{} HTTP/1.1" \
          "\r\n" \
          "Host: {}".format(sys.argv[3], host)
    s.sendall(req.encode())
except IOError as e:
    print("Encountered exception sending file name to server\nErrno:{0}\nError:{1}".format(e.errno, e.strerror))

receiveddata = []
while True:
    received = s.recv(2048)
    if received:
        receiveddata.append(received)
    else:
        break

print(b''.join(receiveddata).decode("utf-8"))