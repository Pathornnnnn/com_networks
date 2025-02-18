
# UDPServer_FlowControl
import socket
import sys

def save_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))

print('The UDP server is ready to receive')

# Receive filename
file_data = {}
filename, clientAddress = serverSocket.recvfrom(1024)
filename = filename.decode()

print(f"Receiving file: {filename}")

expected_sequence = 0

while True:
    packet, clientAddress = serverSocket.recvfrom(4096)

    if packet == b'EOF':
        serverSocket.sendto(b'EOF', clientAddress)
        print("File transfer completed.")
        break

    seq_num = int(packet[:8])
    data = packet[8:]

    # Handle packet duplication and reordering
    if seq_num not in file_data:
        file_data[seq_num] = data

    # Send acknowledgment
    serverSocket.sendto(f'{seq_num}'.encode(), clientAddress)

# Reconstruct the file in the correct order
sorted_data = b''.join(file_data[i] for i in sorted(file_data.keys()))
save_file(filename, sorted_data)
print(f"File {filename} saved successfully.")
