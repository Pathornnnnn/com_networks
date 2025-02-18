import socket
import sys
import os

def read_filename_path(path):
    path = str(path)[::-1]
    name = ''
    for i in path:
        if i == "\\" :
            break
        else:
            name += i
    name = str(name)[::-1]
    return name

filename = read_filename_path(sys.argv[1])
print(filename)
file = os.open(sys.argv[1],os.O_RDWR)
txt = os.read(file,30)
serverName = str(sys.argv[2])
serverPort = int(sys.argv[3])
send_buf_size = 16
recv_buf_size = 16
try:
    recv_buf_size = int(input('Please specify the socket receive buffer size (bytes): '))
    if recv_buf_size < 1:
        print('The receive buffer size is too low!')
        exit(1)
except ValueError:
    print('Input is not a number.')
    exit(2)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf_size) 
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf_size)
clientSocket.connect((serverName, serverPort))

nbyte = recv_buf_size
count = 0
while True:
    strval = input(f"Enter number of bytes to read or enter 0 to end [{nbyte:12d}]: ")
    if strval != '':
        try:
            nbyte = int(strval)
        except ValueError:
            print("Input is not a number. Please try again.")
            continue
        if nbyte <= 0:
            break
    read_data = clientSocket.recv(nbyte)
    print (f"#{count} | Read from buffer: {read_data.decode()}")
    count += 1

clientSocket.close()
