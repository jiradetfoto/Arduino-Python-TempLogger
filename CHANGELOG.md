# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-05-02
### Added (สิ่งที่เพิ่มเข้ามา)
- **Web Dashboard:** Integrated a Flask-based web server to serve a modern environment dashboard using Tailwind CSS and Chart.js.
  - *เพิ่มระบบ Web Dashboard สำหรับดูกราฟและข้อมูลแบบ Real-time ผ่านเบราว์เซอร์*
- **SQLite Integration:** Migrated from CSV storage to a robust SQLite database for better data integrity and querying.
  - *เปลี่ยนระบบเก็บข้อมูลจาก CSV เป็นฐานข้อมูล SQLite เพื่อความเสถียรและการสืบค้นที่รวดเร็ว*
- **Hourly Alignment:** Added logic to precisely align data saves to the start of each hour (e.g., 10:00, 11:00) based on the system clock.
  - *ระบบบันทึกข้อมูลให้ตรงตามต้นชั่วโมงของนาฬิกาคอมพิวเตอร์อัตโนมัติ*
- **Extremes Statistics:** Added API endpoints and UI cards to display Daily, Monthly, and All-Time Max/Min temperature records.
  - *เพิ่มการแสดงสถิติอุณหภูมิสูงสุด-ต่ำสุด รายวัน, รายเดือน และตลอดกาล*
- **System Tray Support:** Added a system tray icon using `pystray` for background operation and easy exit.
  - *เพิ่มไอคอนที่มุมขวาล่าง (System Tray) เพื่อให้รันโปรแกรมเป็นเบื้องหลังได้*
- **PyInstaller Compatibility:** Implemented dynamic path resolution to support running the script as a standalone `.exe`.
  - *ปรับปรุงโค้ดให้รองรับการแปลงเป็นไฟล์ .exe สำหรับใช้งานทั่วไป*

### Changed (สิ่งที่เปลี่ยนแปลง)
- **Architecture Shift:** Moved the hourly average calculation logic from the Arduino firmware to the Python backend to improve hardware stability.
  - *ย้ายการคำนวณค่าเฉลี่ยจากบอร์ด Arduino มาไว้ที่คอมพิวเตอร์ เพื่อให้บอร์ดทำงานได้เสถียรขึ้น*
- **Arduino Firmware:** Simplified the sketch to focus on real-time sensor reading and serial transmission.
  - *ปรับโค้ด Arduino ให้เหลือแค่การอ่านค่าเซนเซอร์และส่งข้อมูลแบบ Real-time*
- **UI Design:** Upgraded the dashboard to a premium Dark Mode / Glassmorphism aesthetic.
  - *ปรับโฉมหน้าเว็บให้ทันสมัยในรูปแบบ Dark Mode และ Glassmorphism*

### Removed (สิ่งที่ตัดออก)
- **CSV Logging:** Legacy CSV logging has been replaced by the SQLite database system.
  - *ยกเลิกการบันทึกข้อมูลลงไฟล์ CSV โดยเปลี่ยนไปใช้ SQLite แทน*

---

## [1.1.0] - 2025-02-28
### Added
- **Auto-Reconnect System:** The Python logger now automatically attempts to reconnect if the Arduino is disconnected.
- **Enhanced Error Handling:** Improved data validation for malformed serial data.

### Fixed
- Fixed an issue where the Python script would terminate upon losing the serial connection.
