
<div align="center">

# 🌡️ Arduino & Python TempLogger (v2.0)
### *Advanced Logging System with SQLite, Web Dashboard & Hourly Stats*

![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Tailwind](https://img.shields.io/badge/-TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)

</div>

---

### 📝 Project Overview (ภาพรวมโครงการ)
ระบบบันทึกอุณหภูมิและความชื้นอัจฉริยะที่เชื่อมต่อระหว่าง Arduino และ Python โดยเวอร์ชันนี้ได้รับการอัปเกรดครั้งใหญ่จากการบันทึก CSV แบบเดิม มาเป็นระบบฐานข้อมูล SQLite พร้อมหน้า Dashboard สวยงามที่ดูผ่านเว็บได้แบบ Real-time

---

## 🚀 Key Features (ฟีเจอร์เด่น)

- ✅ **Web Dashboard:** หน้าจอแสดงผลกราฟเส้นสวยงามด้วย Tailwind CSS และ Chart.js (เข้าดูได้ที่ `http://localhost:5000`)
- ✅ **SQLite Database:** จัดเก็บข้อมูลลงฐานข้อมูลมาตรฐาน มั่นคง และสืบค้นย้อนหลังได้รวดเร็ว
- ✅ **Hourly Alignment:** บันทึกข้อมูลค่าเฉลี่ยทุก "ต้นชั่วโมง" (เช่น 10:00, 11:00) อัตโนมัติ เพื่อความเป็นระเบียบของข้อมูล
- ✅ **Advanced Stats:** คำนวณค่าสูงสุด-ต่ำสุด (Max/Min) ของวัน, เดือน และตลอดกาล พร้อมระบุเวลาที่เกิดขึ้น
- ✅ **Python-Side Averaging:** ย้ายการคำนวณมาที่คอมพิวเตอร์ ทำให้ Arduino ทำงานได้เสถียรขึ้นและไม่สูญเสียข้อมูลหากบอร์ดรีเซ็ต
- ✅ **System Tray:** ทำงานเงียบๆ อยู่ที่มุมขวาล่าง และรองรับการรันแบบซ่อนหน้าต่าง (`pythonw`)

---

## 🛠️ Hardware & Wiring (อุปกรณ์และการต่อวงจร)

- 1️⃣ **Arduino Board** (Uno/Nano)
- 2️⃣ **DHT22 Sensor** (Pin 2)
- 3️⃣ **I2C LCD Display 16x2** (SDA -> A4, SCL -> A5)

---

## 💻 Installation & Usage (การติดตั้งและใช้งาน)

### 1. Arduino Setup
1. ติดตั้ง Library: `DHT sensor library` และ `LiquidCrystal I2C`
2. อัปโหลดโค้ดในโฟลเดอร์ `arduino/sensor_logging/` ลงบอร์ด

### 2. Python Setup
1. ติดตั้ง Python 3.x
2. ติดตั้ง Libraries ที่จำเป็น:
   ```bash
   pip install pyserial pystray Pillow flask
   ```

### 3. Start Program
รันสคริปต์หลัก:
```bash
python python/DHT22.py
```
*หรือถ้าไม่ต้องการให้เห็นหน้าต่างจอดำ:*
```bash
pythonw python/DHT22.py
```

### 4. View Dashboard
เปิดเว็บเบราว์เซอร์ไปที่: 👉 **http://localhost:5000**

---

## 📂 File Structure
- `arduino/` → โค้ดสำหรับบอร์ด Arduino
- `python/` → สคริปต์หลัก Python และหน้าเว็บ Dashboard
- `python/templates/` → ไฟล์ HTML Dashboard
- `python/sensor_log.db` → ไฟล์ฐานข้อมูล SQLite (จะถูกสร้างขึ้นอัตโนมัติ)

---

### ⚙️ Configuration
คุณสามารถปรับแต่งการตั้งค่าได้ใน `python/DHT22.py`:
- `BAUD_RATE`: ความเร็วการเชื่อมต่อ (Default: 9600)
- `Port Detection`: ระบบจะค้นหา Arduino ให้อัตโนมัติ

<br>
Developed with ❤️ by a passionate Arduino beginner.
