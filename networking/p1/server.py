#import socket module
from socket import *
from datetime import date
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
#Fill in start
serverSocket.bind(("0.0.0.0", 6789))
serverSocket.listen()
#Fill in end

while True:
    #Establish the connection
    print("Ready to serve on {}".format(gethostbyname(gethostname())))
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(2048)
        if not message:
            print("received no data from socket.")
            continue

        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        #Send one HTTP header line into socket
        success =   "HTTP/1.1 200 OK\r\n" \
                    "Content-Length: {}\r\n" \
                    "Connection: Closed\r\n" \
                    "Content-Type: text/html; charset=utf-8\r\n\r\n".format(len(outputdata))
        connectionSocket.send(success.encode())

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError as e:
        #Send response message for file not found (404)
        doc =   "<html>" \
                    "<head>" \
                        "<title>404 Not Found</title>" \
                    "</head>" \
                    "<body>" \
                        "<h1>Not Found</h1>" \
                        "<p>The requested resource <strong>{}</strong> was not found on this server.</p>" \
                    "</body>" \
                "</html>".format(filename.decode())
        notfound = "HTTP/1.1 404 Not Found\r\n" \
                   "Date: {}\r\n" \
                   "Server: reutann server\r\n" \
                   "Content-Length: {}\r\n" \
                   "Connection: Closed\r\n" \
                   "Content-Type: text/html; charset=utf-8\r\n" \
                   .format(date.today(), len(doc))
        connectionSocket.send("{}\r\n{}".format(notfound, doc).encode())
        #Close client socket
        connectionSocket.close()
serverSocket.close()
sys.exit()  #Terminate the program after sending the corresponding data


