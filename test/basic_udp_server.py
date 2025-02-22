import socket

# สร้าง UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# กำหนด IP และ Port ที่จะรับข้อมูล
server_address = ('127.0.0.1', 12345)
server_socket.bind(server_address)

print(f"UDP Server กำลังรอข้อมูลที่ {server_address}")

while True:
    data, client_address = server_socket.recvfrom(1024)  # รับข้อมูลขนาดสูงสุด 1024 ไบต์
    print(f"ได้รับข้อความจาก {client_address}: {data.decode('utf-8')}")

    # ส่งข้อความตอบกลับ
    server_socket.sendto(b"recive message ! :", client_address)
