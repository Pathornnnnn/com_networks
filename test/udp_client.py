import socket
import sys
import os

# สร้าง UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
file_path = "D:\Code\com_network\data.txt"
filename = os.path.basename(file_path)
# serverName = str(sys.argv[2])
# serverPort = int(sys.argv[3])

# กำหนด IP และ Port ของ Server
server_address = ('127.0.0.1', 12345)

try:
    while True:
        client_socket.sendto(filename.encode(), server_address)
        message = input("ป้อนข้อความ: ")
        client_socket.sendto(message.encode('utf-8'), server_address)  # ส่งข้อความ

        # รอข้อความตอบกลับ
        data, _ = client_socket.recvfrom(1024)
        print(f"ข้อความจาก Server: {data.decode('utf-8')}")
finally:
    client_socket.close()
