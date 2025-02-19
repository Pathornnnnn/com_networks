
# UDP Server
import socket
import os

# สร้าง UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# กำหนด IP และ Port ที่จะรับข้อมูล
server_address = ('127.0.0.1', 12345)
server_socket.bind(server_address)

print(f"UDP Server กำลังรอข้อมูลที่ {server_address}")

file = None

try:
    while True:
        data, client_address = server_socket.recvfrom(4096)

        # หากยังไม่มีไฟล์ ให้รับชื่อไฟล์
        if not file:
            filename = data.decode('utf-8')
            print(f"สร้างไฟล์ใหม่: {filename}")
            file = open('n_'+filename, 'wb')
            server_socket.sendto(b"Filename received", client_address)
            continue

        # ตรวจสอบการสิ้นสุดการส่งข้อมูล
        if data == b"END_OF_FILE":
            print("ได้รับข้อมูลครบถ้วน ปิดไฟล์")
            break

        # ดึง sequence number (4 ไบต์แรก) และข้อมูล
        sequence_number = int.from_bytes(data[:4], 'big')
        message = data[4:]

        print(f"[Seq {sequence_number}] จาก {client_address}: รับข้อมูล {len(message)} ไบต์")

        # เขียนข้อมูลไบนารีลงไฟล์
        file.write(message)

        # ส่งข้อความตอบกลับ
        server_socket.sendto(b"Received message"+b': '+str(sequence_number).encode('utf-8'), client_address)

finally:
    if file:
        file.close()
    server_socket.close()
