# Project Log: Arduino-Python-TempLogger

## Progress Summary (Session: May 2026)

### ✅ Completed Features
1. **Database Migration:**
   - เปลี่ยนจาก CSV เป็น SQLite (`sensor_log.db`) เพื่อความทนทานและการสืบค้นข้อมูลที่รวดเร็ว
   - เพิ่มระบบคำนวณค่าสถิติสูงสุด-ต่ำสุด (Max/Min) รายวัน, รายเดือน และตลอดกาลผ่าน SQL Query

2. **Architecture Optimization:**
   - ย้ายตรรกะการคำนวณค่าเฉลี่ยจาก Arduino มาไว้ที่ Python 100%
   - ปรับปรุงให้ Arduino ส่งค่าดิบ (RAW_T, RAW_H) ทุก 2.5 วินาที ลดภาระการประมวลผลบนบอร์ด
   - แก้ไขระบบการบันทึกให้ตรงตาม "ต้นชั่วโมง" ของนาฬิกาคอมพิวเตอร์ (เช่น 14:00, 15:00) แม้จะเริ่มรันโปรแกรมในเวลาใดก็ตาม

3. **Web Dashboard Dashboard:**
   - พัฒนาหน้าเว็บด้วย Tailwind CSS ดีไซน์แบบ Modern Dark Mode / Glassmorphism
   - ใช้ Chart.js แสดงกราฟเส้นย้อนหลัง 24 ชั่วโมง โดยสลับแกนอุณหภูมิไว้ด้านขวาตามความต้องการผู้ใช้
   - เพิ่มการ์ดสถิติ Max/Min พร้อมระบุวันเวลาที่เกิดขึ้นจริง

4. **Desktop Integration:**
   - รองรับการทำงานใน System Tray (มุมขวาล่าง)
   - รองรับการรันแบบไร้หน้าต่าง (Windowless) ผ่าน `pythonw.exe`

### 🛠️ Maintenance & Compatibility
- ปรับปรุงโค้ดให้รองรับการรันผ่าน PyInstaller (กรณีต้องการแปลงเป็น .exe ในอนาคต) โดยใช้ระบบหา Path แบบ Dynamic
- เพิ่มระบบ Debug Log ในตัวสคริปต์เพื่อตรวจสอบสถานะ Buffer และเวลานับถอยหลังการบันทึก

### 📅 Status
- **Current Status:** Stable & Functional
- **Next Steps:** (Optional) เพิ่มการแจ้งเตือนผ่าน LINE Notify เมื่ออุณหภูมิเกินกำหนด หรือเพิ่มระบบ Export ข้อมูลจาก SQLite กลับเป็น Excel/CSV
