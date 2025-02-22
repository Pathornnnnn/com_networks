# UDP Client
import socket
import os
import time

# สร้าง UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(2)  # ตั้งเวลา timeout 2 วินาที

file_path = "D:/Code/com_network/test_1MB.txt"
filename = os.path.basename(file_path)

# กำหนด IP และ Port ของ Server
server_address = ('127.0.0.1', 12345)

CHUNK_SIZE = 1024

try:
    sequence_number = 0

    # ส่งชื่อไฟล์ไปยัง Server
    client_socket.sendto(filename.encode(), server_address)

    # รอการยืนยันจาก Server
    try:
        data, _ = client_socket.recvfrom(1024)
        print(f"Server: {data.decode('utf-8')}")
    except socket.timeout:
        print("Error: ไม่ได้รับการตอบกลับจาก Server")
        exit(1)

    # เปิดไฟล์ในโหมดไบนารี
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break

            # รวม sequence number (4 ไบต์) กับข้อมูล
            data_packet = sequence_number.to_bytes(4, 'big') + chunk

            # ส่งข้อมูลไปยัง Server พร้อม retry (สูงสุด 5 ครั้ง)
            retries = 0
            while retries < 5:
                try:
                    client_socket.sendto(data_packet, server_address)
                    data, _ = client_socket.recvfrom(1024)

                    # ตรวจสอบ ACK
                    ack_number = int.from_bytes(data, 'big')
                    if ack_number == sequence_number:
                        print(f"[Client] ส่งข้อมูลสำเร็จ: Seq {sequence_number}")
                        break  # ออกจาก loop หากส่งสำเร็จ
                except socket.timeout:
                    retries += 1
                    print(f"[Client] Timeout! ส่งใหม่: Seq {sequence_number} (Retry {retries})")

            if retries == 5:
                print(f"[Client] ล้มเหลวในการส่ง: Seq {sequence_number}")
                exit(1)

            sequence_number += 1

    # ส่งข้อความสิ้นสุดการส่งข้อมูล
    client_socket.sendto(b"END_OF_FILE", server_address)

finally:
    client_socket.close()

