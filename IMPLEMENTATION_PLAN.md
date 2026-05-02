# Implementation Plan: SQLite Migration, Architecture Update & Web Dashboard

## App features and User Stories
- **Phase 1: SQLite Storage (Completed):** เปลี่ยนการบันทึกข้อมูลจากไฟล์ CSV เป็นฐานข้อมูล SQLite เพื่อรองรับข้อมูลจำนวนมากและให้สืบค้น (Query) ย้อนหลังได้ง่ายขึ้น
- **Phase 2: Move Average Calculation to Python (Completed):** ย้ายตรรกะการคำนวณค่าเฉลี่ยมาที่ Python เพื่อลดภาระ Arduino และป้องกันข้อมูลสูญหายเวลาไฟตก
- **Phase 3: Web Dashboard (New):**
  - สร้าง Web Application ขนาดเล็กที่เสิร์ฟจาก Python โดยตรง (ไม่ต้องจำลองเซิร์ฟเวอร์แยกต่างหาก)
  - มีหน้า Dashboard ที่แสดงกราฟเส้น (Line Chart) เพื่อดูแนวโน้มอุณหภูมิและความชื้นย้อนหลัง
  - รองรับการแสดงผลแบบ Responsive และดีไซน์สวยงามทันสมัยด้วย Tailwind CSS
- **User Story:** ในฐานะผู้ใช้งาน ฉันสามารถเปิด Web Browser (เช่น Chrome) ไปที่ `http://localhost:5000` แล้วดูรูปกราฟอุณหภูมิของห้องฉันได้ทันที โดยกราฟจะดึงข้อมูลจาก SQLite ขึ้นมาแสดงผลอย่างสวยงาม

## Project architecture and Folder structure
- `arduino/sensor_logging.ino` *(ไม่ต้องแก้ไข)*
- `python/DHT22.py` *(แก้ไข: เพิ่มระบบ Thread สำหรับรัน Web Server (Flask) พร้อมกับระบบเดิม)*
- `python/sensor_log.db` *(ฐานข้อมูล SQLite)*
- `python/templates/index.html` *(ไฟล์ใหม่: หน้าตาของ Web Dashboard)*

## Tech stack
- **Backend Language:** Python 3 (รวมการอ่าน Hardware และรัน Web API ด้วยไลบรารี `Flask`)
- **Database:** SQLite
- **Frontend / UI:** 
  - **CSS Framework:** Tailwind CSS (โหลดผ่าน CDN เพื่อความง่าย, สอดคล้องกับ Priority Rule)
  - **Graph Library:** Chart.js (สำหรับวาดกราฟแบบ Interactive)
  - **Structure:** HTML5, Vanilla JS
