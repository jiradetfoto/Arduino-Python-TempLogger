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
import sqlite3
from flask import Flask, render_template, jsonify
import logging

# --- ฟังก์ชันจัดการ Path สำหรับ PyInstaller ---
def get_base_path():
    if getattr(sys, 'frozen', False):
        # ถ้าเป็นไฟล์ .exe (Frozen) ให้ใช้ตำแหน่งที่ไฟล์ .exe ตั้งอยู่
        # เพื่อให้หาโฟลเดอร์ templates และฐานข้อมูลที่อยู่นอกไฟล์ .exe เจอ
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

script_dir = get_base_path()
BAUD_RATE = 9600
DB_FILENAME = os.path.join(script_dir, 'sensor_log.db')
ICON_FILE = os.path.join(script_dir, 'icons8.ico') # ชื่อไฟล์ไอคอน

stop_event = threading.Event()

buffer_lock = threading.Lock()
data_buffer = []
rolling_buffer = []

app = Flask(__name__, template_folder=os.path.join(script_dir, 'templates'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/current')
def get_current():
    try:
        with buffer_lock:
            if not rolling_buffer:
                return jsonify({'temperature': None, 'humidity': None, 'timestamp': None})
            
            avg_t = sum(item[1] for item in rolling_buffer) / len(rolling_buffer)
            avg_h = sum(item[2] for item in rolling_buffer) / len(rolling_buffer)
            return jsonify({
                'temperature': avg_t, 
                'humidity': avg_h, 
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data')
def get_data():
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        # ดึง 24 ตัวอย่างล่าสุด (เช่น 24 ชั่วโมง)
        cursor.execute("SELECT timestamp, temperature, humidity FROM sensor_data ORDER BY id DESC LIMIT 24")
        rows = cursor.fetchall()
        conn.close()
        
        # คืนค่าแบบเรียงจากเก่าไปใหม่ (ASC) เพื่อวาดกราฟซ้ายไปขวา
        data = [{'timestamp': r[0], 'temperature': r[1], 'humidity': r[2]} for r in reversed(rows)]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        
        now = datetime.datetime.now()
        today_str = now.strftime('%Y-%m-%d') + '%'
        month_str = now.strftime('%Y-%m') + '%'
        
        stats = {}
        
        def fetch_max_min(prefix):
            if prefix:
                cursor.execute("SELECT timestamp, temperature FROM sensor_data WHERE timestamp LIKE ? ORDER BY temperature DESC LIMIT 1", (prefix,))
                max_row = cursor.fetchone()
                cursor.execute("SELECT timestamp, temperature FROM sensor_data WHERE timestamp LIKE ? ORDER BY temperature ASC LIMIT 1", (prefix,))
                min_row = cursor.fetchone()
            else:
                cursor.execute("SELECT timestamp, temperature FROM sensor_data ORDER BY temperature DESC LIMIT 1")
                max_row = cursor.fetchone()
                cursor.execute("SELECT timestamp, temperature FROM sensor_data ORDER BY temperature ASC LIMIT 1")
                min_row = cursor.fetchone()
            
            return {
                'max': {'temp': max_row[1], 'time': max_row[0]} if max_row else None,
                'min': {'temp': min_row[1], 'time': min_row[0]} if min_row else None
            }

        stats['today'] = fetch_max_min(today_str)
        stats['month'] = fetch_max_min(month_str)
        stats['all_time'] = fetch_max_min(None)
        
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_flask():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR) # ปิด log ของ Flask ไม่ให้รก terminal
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# ฟังก์ชันเดิม(คงไว้เหมือนเดิม)
def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    arduino_identifiers = ["Arduino", "CH340", "USB Serial", "FTDI", "CP210"]
    for p in ports:
        for identifier in arduino_identifiers:
            if identifier in p.description:
                return p.device
    return None

def init_db():
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database Initialization Error: {e}")



def insert_to_db(timestamp, temperature, humidity):
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_data (timestamp, temperature, humidity)
            VALUES (?, ?, ?)
        ''', (timestamp, temperature, humidity))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"ERROR: Database write failed. {e}")

def average_and_save_worker():
    while not stop_event.is_set():
        # คำนวณเวลาวินาทีที่เหลือจนกว่าจะถึง "ต้นชั่วโมง" ถัดไป (เช่น 10:00:00)
        now = datetime.datetime.now()
        next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        seconds_to_wait = int((next_hour - now).total_seconds())
        
        # รอจนกว่าจะถึงต้นชั่วโมง (เช็คทีละ 1 วินาที เพื่อให้กดปิดโปรแกรมได้ทันที)
        for i in range(seconds_to_wait):
            if stop_event.is_set():
                return
            
            # ปริ้นสถานะทุกๆ 1 นาที เพื่อให้รู้ว่าโปรแกรมยังทำงานอยู่
            if (seconds_to_wait - i) % 60 == 0 or i == 0:
                with buffer_lock:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ⏳ Next save in: {seconds_to_wait - i}s | Buffer size: {len(data_buffer)} samples")
            
            time.sleep(1)
            
        with buffer_lock:
            if len(data_buffer) > 0:
                avg_t = sum(item[0] for item in data_buffer) / len(data_buffer)
                avg_h = sum(item[1] for item in data_buffer) / len(data_buffer)
                
                # ใช้เวลาต้นชั่วโมงนั้นๆ เป็น Timestamp ให้ตรงเป๊ะ (เช่น 10:00:00)
                timestamp = next_hour.strftime('%Y-%m-%d %H:00:00')
                
                print(f"[{timestamp}] 📊 Hourly Average: T={avg_t:.2f}C, H={avg_h:.2f}% (from {len(data_buffer)} samples)")
                insert_to_db(timestamp, avg_t, avg_h)
                
                data_buffer.clear()

def send_heartbeat(ser):
    while not stop_event.is_set():
        try:
            ser.write(b'P')
            time.sleep(5)
        except:
            break

# ฟังก์ชันหลักที่รัน Logic ของ Arduino (แยกออกมาเป็น Thread)
def sensor_logic():
    init_db()
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
                    if line and line.startswith("RAW_T:"):
                        try:
                            parts = line.split(',')
                            t_val = float(parts[0].split(':')[1])
                            h_val = float(parts[1].split(':')[1])
                            
                            with buffer_lock:
                                data_buffer.append((t_val, h_val))
                                
                                current_time = time.time()
                                rolling_buffer.append((current_time, t_val, h_val))
                                # จำกัดข้อมูลให้เหลือแค่ 10 นาทีล่าสุด (600 วินาที)
                                while rolling_buffer and current_time - rolling_buffer[0][0] > 600:
                                    rolling_buffer.pop(0)

                                # ปริ้นทุกๆ 100 samples เพื่อยืนยันว่าข้อมูลเข้า (ประมาณทุก 4 นาที)
                                if len(data_buffer) % 100 == 0:
                                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Received 100 new samples from Arduino.")
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
    
    # รันตัวคำนวณค่าเฉลี่ย
    avg_thread = threading.Thread(target=average_and_save_worker, daemon=True)
    avg_thread.start()
    
    # รัน Web Dashboard Server
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # รัน Tray (ฟังก์ชันนี้จะ Block การทำงานจนกว่าจะปิด Tray)
    icon.run()

if __name__ == "__main__":
    setup_tray()