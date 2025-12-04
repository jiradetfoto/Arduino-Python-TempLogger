
<div align="center">

# 🌡️ Arduino & Python Temperature Logger
### *Automated Logging System with Anti-Flicker LCD & Auto-Port Detection*

![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

### 📝 Note from the Creator / หมายเหตุจากผู้สร้าง
> "Hi! I am a beginner just learning how to use Arduino. This project represents my journey in understanding sensors, serial communication, and Python integration. I've tried my best to make the code robust and stable. Feel free to use it or give suggestions!"
>
> "สวัสดี!  ฉันเป็นมือใหม่ที่เพิ่งหัดใช้ Arduino โปรเจกต์นี้คือผลลัพธ์จากการเรียนรู้เรื่องเซ็นเซอร์ การสื่อสารผ่าน Serial และการเขียนโปรแกรมร่วมกับ Python ฉันพยายามปรับปรุงโค้ดให้ทำงานได้เสถียรที่สุดเท่าที่จะทำได้ สามารถนำไปใช้หรือแนะนำติชมได้!"

---

## 🎨 Project Canvas (ภาพรวมโครงการ)

| 🚀 **Key Features (ฟีเจอร์เด่น)** | 🛠️ **Hardware Required (อุปกรณ์ที่ใช้)** |
| :--- | :--- |
| ✅ **Auto-Detect Port:** Python finds Arduino automatically.<br>✅ **Anti-Flicker LCD:** Smooth real-time display.<br>✅ **Statistically Accurate:** Calculates valid hourly averages.<br>✅ **Heartbeat System:** Detects PC disconnection in 12s.<br>✅ **Dual Mode:** Display-only (Offline) & Logging (Online). | 1️⃣ **Arduino Board** (Uno/Nano)<br>2️⃣ **DHT22 Sensor** (Temp/Humid)<br>3️⃣ **I2C LCD Display** (16x2)<br>4️⃣ **Jumper Wires & Breadboard** |

| 🔌 **Wiring Diagram (การต่อวงจร)** | 📂 **File Structure (โครงสร้างไฟล์)** |
| :--- | :--- |
| **DHT22** → `Pin 2` (VCC/GND)<br>**I2C LCD (SDA)** → `Pin A4`<br>**I2C LCD (SCL)** → `Pin A5`<br>**Power** → `5V / GND` | `arduino/` → `sensor_logging.ino`<br>`python/` → `logger.py`<br>`data/` → `sensor_log_1hour.csv`<br>`README.md` → Documentation |

---

## 💻 Installation & Usage (การติดตั้งและใช้งาน)

### 1️⃣ Arduino Setup (ฝั่งบอร์ด)
1. Install **Arduino IDE**.
2. Install Libraries: `DHT sensor library` & `LiquidCrystal I2C`.
3. Upload **`sensor_logging.ino`**.

### 2️⃣ Python Setup (ฝั่งคอมพิวเตอร์)
1. Install **Python 3.x**.
2. Install library:
   ```bash
   pip install pyserial


### 3️⃣ Start Logging (เริ่มใช้งาน)

Run the script:

```bash
python logger.py
```

> **Result:** The LCD will show **"PC"** at the bottom-right corner. Data will be saved to CSV every hour.

-----



### ⚙️ Configuration (การตั้งค่า)

| Variable | File | Description | Default |
| :--- | :--- | :--- | :--- |
| `SAMPLE_INTERVAL_MS` | Arduino | Reading frequency | `2500` (2.5s) |
| `SAMPLES_PER_HOUR` | Arduino | Samples per log cycle | `1440` |
| `CSV_FILENAME` | Python | Output file name | `sensor_log_1hour.csv` |

<br>
i Developed with ❤️ by a passionate Arduino beginner.

