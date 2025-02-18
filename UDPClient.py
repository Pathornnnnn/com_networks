# UDPClient_FlowControl
import socket
import sys
import os
import time
import threading

def read_filename_path(path):
    path = str(path)[::-1]
    name = ''
    for i in path:
        if i == "\\":
            break
        else:
            name += i
    return str(name)[::-1]

def read_file_chunks(file_path, chunk_size):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

filename = read_filename_path(sys.argv[1])
file_path = sys.argv[1]
serverName = str(sys.argv[2])
serverPort = int(sys.argv[3])

send_buf_size = 1024  # Packet size

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(1)  # Set timeout for retransmissions

# Send the filename first
clientSocket.sendto(filename.encode(), (serverName, serverPort))

# Send the file data with acknowledgments
sequence_number = 0
lock = threading.Lock()
acks_received = set()

def receive_acks():
    global acks_received
    while True:
        try:
            ack, _ = clientSocket.recvfrom(1024)
            ack_num = int(ack.decode())
            with lock:
                acks_received.add(ack_num)
        except socket.timeout:
            break

# Start ACK receiver thread
ack_thread = threading.Thread(target=receive_acks)
ack_thread.daemon = True
ack_thread.start()

for chunk in read_file_chunks(file_path, send_buf_size):
    packet = f'{sequence_number:08d}'.encode() + chunk
    while True:
        clientSocket.sendto(packet, (serverName, serverPort))
        time.sleep(0.01)  # Simulate network latency
        with lock:
            if sequence_number in acks_received:
                break
        print(f"Timeout or packet loss, resending packet {sequence_number}")

    sequence_number += 1

# Send end-of-file marker
while True:
    clientSocket.sendto(b'EOF', (serverName, serverPort))
    time.sleep(0.01)
    with lock:
        if 'EOF' in acks_received:
            break

clientSocket.close()
print("File transfer complete.")
