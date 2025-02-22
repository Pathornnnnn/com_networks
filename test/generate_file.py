# สร้างไฟล์ขนาด 1 MiB (1048576 bytes)
import os
with open('test_1MB.txt', 'wb') as f:
    f.write(os.urandom(1048576))

print("✅ สร้างไฟล์ test_1MB.txt สำเร็จ!")
