import serial
import serial.tools.list_ports
import time
import datetime
import csv
import os
import threading
import pystray
from PIL import Image
import sys

# --- ตั้งค่าเดิม ---
BAUD_RATE = 9600
CSV_FILENAME = 'sensor_log_1hour.csv'
ICON_FILE = 'icons8.ico' # ชื่อไฟล์ไอคอน

stop_event = threading.Event()

# ฟังก์ชันเดิม(คงไว้เหมือนเดิม)
def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    arduino_identifiers = ["Arduino", "CH340", "USB Serial", "FTDI", "CP210"]
    for p in ports:
        for identifier in arduino_identifiers:
            if identifier in p.description:
                return p.device
    return None

def check_and_write_header():
    if not os.path.isfile(CSV_FILENAME):
        try:
            with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(['Timestamp', 'Avg_Temperature_C', 'Avg_Humidity_Perc'])
        except IOError as e:
            print(f"ERROR: {e}")

def append_to_csv(data_row):
    try:
        with open(CSV_FILENAME, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(data_row)
            f.flush()
    except IOError as e:
        print(f"ERROR: Write failed. {e}")

def send_heartbeat(ser):
    while not stop_event.is_set():
        try:
            ser.write(b'P')
            time.sleep(5)
        except:
            break

# ฟังก์ชันหลักที่รัน Logic ของ Arduino (แยกออกมาเป็น Thread)
def sensor_logic():
    check_and_write_header()
    while not stop_event.is_set():
        target_port = find_arduino_port()
        if target_port is None:
            time.sleep(5)
            continue
        try:
            with serial.Serial(target_port, BAUD_RATE, timeout=2) as ser:
                time.sleep(2)
                ser.write(b'S')
                hb_thread = threading.Thread(target=send_heartbeat, args=(ser,), daemon=True)
                hb_thread.start()
                while not stop_event.is_set():
                    try:
                        line = ser.readline().decode('utf-8', errors='ignore').strip()
                    except (serial.SerialException, OSError):
                        break
                    if line and line.startswith("AVG_T:"):
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        try:
                            parts = line.split(',')
                            t_val = float(parts[0].split(':')[1])
                            h_val = float(parts[1].split(':')[1])
                            append_to_csv([timestamp, t_val, h_val])
                        except:
                            pass
        except:
            time.sleep(2)

# --- ส่วนของ System Tray ---
def on_quit(icon, item):
    stop_event.set() # สั่งหยุด Thread ทั้งหมด
    icon.stop() # ปิดไอคอน
    sys.exit()

def setup_tray():
    # โหลดไอคอน
    try:
        image = Image.open(ICON_FILE)
    except:
        # ถ้าไม่มีไฟล์ไอคอน ให้สร้างสี่เหลี่ยมสีเขียวขึ้นมาแทน
        image = Image.new('RGB', (64, 64), color=(0, 128, 0))

    menu = (pystray.MenuItem('Exit', on_quit),)
    icon = pystray.Icon("DHT22_Monitor", image, "DHT22 Data Logger", menu)
    
    # รันเซนเซอร์ในเบื้องหลัง
    thread = threading.Thread(target=sensor_logic, daemon=True)
    thread.start()
    
    # รัน Tray (ฟังก์ชันนี้จะ Block การทำงานจนกว่าจะปิด Tray)
    icon.run()

if __name__ == "__main__":
    setup_tray()