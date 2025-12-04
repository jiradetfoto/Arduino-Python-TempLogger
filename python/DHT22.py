import serial
import serial.tools.list_ports
import time
import datetime
import csv
import os
import threading

# --- ตั้งค่า ---
BAUD_RATE = 9600
CSV_FILENAME = 'sensor_log_1hour.csv'

stop_event = threading.Event()

# ฟังก์ชันหา Port อัตโนมัติ
def find_arduino_port():
    print("Scanning ports...")
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
            print(f"Created new log file: {CSV_FILENAME}")
        except IOError as e:
            print(f"ERROR: {e}")

def append_to_csv(data_row):
    try:
        with open(CSV_FILENAME, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(data_row)
            f.flush()
    except IOError as e:
        print(f"ERROR: Write failed. {e}")

# Thread ส่ง Heartbeat 'P' ทุก 5 วินาที
def send_heartbeat(ser):
    while not stop_event.is_set():
        try:
            ser.write(b'P')
            time.sleep(5)
        except:
            break

def main():
    check_and_write_header()
    
    target_port = find_arduino_port()
    if target_port is None:
        print("❌ Arduino not found! Please check USB.")
        return

    print(f"✅ Connecting to: {target_port} ...")

    try:
        with serial.Serial(target_port, BAUD_RATE, timeout=2) as ser:
            time.sleep(2) 
            
            # ส่ง 'S' เริ่มต้น
            ser.write(b'S')
            print("Connected! Waiting for 60-minute average data...")
            
            # เริ่ม Heartbeat
            hb_thread = threading.Thread(target=send_heartbeat, args=(ser,), daemon=True)
            hb_thread.start()

            while True:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                except serial.SerialException:
                    print("Connection lost.")
                    break

                if line:
                    if line.startswith("AVG_T:") and ",AVG_H:" in line:
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        try:
                            parts = line.split(',')
                            t_val = float(parts[0].split(':')[1])
                            h_val = float(parts[1].split(':')[1])

                            print(f"[{timestamp}] 📥 Received: T={t_val:.2f}C, H={h_val:.2f}%")
                            append_to_csv([timestamp, t_val, h_val])
                        except ValueError:
                            pass
                    else:
                        print(f"[Device]: {line}")

    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        stop_event.set()

if __name__ == "__main__":
    main()