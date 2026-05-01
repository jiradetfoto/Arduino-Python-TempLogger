# Implementation Plan: SQLite Migration

## App features and User Stories
- **Feature 1: SQLite Storage:** เปลี่ยนการบันทึกข้อมูลจากไฟล์ CSV เป็นฐานข้อมูล SQLite เพื่อรองรับข้อมูลจำนวนมากและให้สืบค้น (Query) ย้อนหลังได้ง่ายขึ้น
- **Feature 2: CSV to SQLite Migration (Auto-import):** ระบบจะตรวจสอบว่ามีไฟล์ CSV เดิม (`sensor_log_1hour.csv`) อยู่หรือไม่ หากมี ระบบจะอ่านข้อมูลทั้งหมดและ import เข้าไปในฐานข้อมูล SQLite อัตโนมัติ จากนั้นจะเปลี่ยนชื่อไฟล์เก่าเป็น `sensor_log_1hour_backup.csv` เพื่อป้องกันการ import ซ้ำและเก็บไว้เป็น Backup
- **User Story:** ในฐานะผู้ใช้งาน เมื่อฉันรันสคริปต์ Python เวอร์ชันใหม่ ข้อมูลเก่าที่เคยเก็บไว้ใน CSV จะถูกย้ายเข้าสู่ SQLite ให้โดยอัตโนมัติ (ไม่สูญหาย) และสคริปต์จะเริ่มบันทึกข้อมูลใหม่ต่อใน SQLite ทันทีโดยที่ฉันไม่ต้องทำอะไรเพิ่มเติม

## Project architecture and Folder structure
โครงสร้างโปรเจกต์ส่วนใหญ่ยังคงเดิม แต่จะมีการเพิ่มไฟล์ Database และแก้ไขสคริปต์หลัก:
- `arduino/sensor_logging.ino` *(ไม่มีการเปลี่ยนแปลง)*
- `python/DHT22.py` *(แก้ไขเพื่อลบระบบเขียน CSV ออก, เพิ่มระบบเชื่อมต่อ SQLite, และเพิ่มฟังก์ชัน import CSV)*
- `python/sensor_log.db` *(ไฟล์ฐานข้อมูล SQLite ใหม่ที่จะถูกสร้างขึ้นอัตโนมัติ)*

## Tech stack
โปรเจกต์นี้เป็น Python Desktop Script จึงใช้เทคโนโลยีดังนี้:
- **Language:** Python 3
- **Database:** SQLite (ใช้ไลบรารี `sqlite3` ซึ่งเป็น Built-in ของ Python ไม่ต้องติดตั้งเพิ่มเติม)
- **Dependencies:** `pyserial` (สำหรับต่อกับ Arduino), `csv`, `os`, `datetime`
*(หมายเหตุ: ไม่ได้ใช้งาน PHP, Next.js, Tailwind CSS หรือ Expo ตามที่กำหนดไว้เป็น Priority เนื่องจากโปรเจกต์นี้เป็น Backend Service สำหรับอ่านค่าฮาร์ดแวร์)*
