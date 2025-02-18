import socket
import sys

print(sys.argv[1],sys.argv[2])
serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])

quotes = []
quotes.append("The Internet is literally a network of networks.")
quotes.append("The Internet lives where anyone can access it.")
quotes.append("The idea that you can somehow erase the Internet is silly.")

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(8)
print('The server is ready to receive')

while True:
     connectionSocket, addr = serverSocket.accept()
     for quote in quotes:
          connectionSocket.send(quote.encode())
     connectionSocket.close()
