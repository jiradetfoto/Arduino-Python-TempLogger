#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

// --- ตั้งค่าฮาร์ดแวร์ ---
#define DHTPIN 2
#define DHTTYPE DHT22
const int LCD_ADDRESS = 0x27; // หรือ 0x3F ตามรุ่นจอ

// --- Config เวลา ---
// อ่านทุก 2.5 วินาที (เพื่อให้ DHT22 อ่านได้แม่นยำและเสถียรที่สุด)
const unsigned long SAMPLE_INTERVAL_MS = 2500; 
// 1 ชั่วโมง (3600 วิ) / 2.5 วิ = 1440 ตัวอย่าง
const int SAMPLES_PER_HOUR = 1440;    
const unsigned long HEARTBEAT_TIMEOUT = 12000; // 12 วินาที

// --- ออบเจ็กต์ ---
DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(LCD_ADDRESS, 16, 2);

// --- ตัวแปรคำนวณ ---
double tempSum = 0.0;
double humidSum = 0.0;
unsigned long sampleCount = 0; // นับจำนวนที่อ่านได้จริง

float currentT = NAN;
float currentH = NAN;

unsigned long lastSampleTime = 0;
unsigned long lastHeartbeatTime = 0;

bool isLoggingMode = false;
bool isTemplatePrinted = false;

// --- ส่งข้อมูลไป PC ---
void sendToPC(float t, float h) {
  Serial.print("AVG_T:");
  Serial.print(t, 1);
  Serial.print(",AVG_H:");
  Serial.println(h, 1);
}

// --- แสดงผล LCD (แบบนิ่งสนิท ไม่กะพริบ) ---
void displayCurrentOnLCD(float t, float h) {
  if (isnan(t) || isnan(h)) {
    lcd.clear();
    lcd.print("Sensor Error...");
    isTemplatePrinted = false; // ถ้า Error ต้องพิมพ์ Template ใหม่เมื่อหาย
    return;
  }

  // พิมพ์ข้อความหลักแค่ครั้งเดียว
  if (!isTemplatePrinted) {
    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("Now T:"); 
    lcd.setCursor(0, 1); lcd.print("Now H:"); 
    isTemplatePrinted = true;
  }
  
  // เทคนิค: เขียนเลขใหม่ทับเลขเดิม + เว้นวรรคยาวๆ ("C   ") เพื่อลบเศษเลขเก่า
  lcd.setCursor(7, 0); lcd.print(t, 1); lcd.print("C   ");
  lcd.setCursor(7, 1); lcd.print(h, 1); lcd.print("%   ");

  // แสดงสถานะ PC
  lcd.setCursor(14, 1); 
  if (isLoggingMode) lcd.print("PC"); else lcd.print("  ");
}

// --- ตรวจสอบการเชื่อมต่อ ---
void checkSerialConnection() {
  // เช็ค Heartbeat Timeout
  if (isLoggingMode && (millis() - lastHeartbeatTime > HEARTBEAT_TIMEOUT)) {
    isLoggingMode = false; 
    displayCurrentOnLCD(currentT, currentH); // ลบคำว่า PC
  }

  // รับคำสั่งจาก PC
  while (Serial.available() > 0) {
    char cmd = Serial.read();

    if (cmd == 'S' || cmd == 'P') { 
      lastHeartbeatTime = millis();
      if (!isLoggingMode) {
        isLoggingMode = true;
        displayCurrentOnLCD(currentT, currentH); // แสดง PC ทันที
      }
    }
  }
}

void setup() {
  Serial.begin(9600);
  lcd.begin(); 
  lcd.backlight();
  dht.begin();
  
  lcd.print("System Starting...");
  delay(1000);

  float t = dht.readTemperature();
  float h = dht.readHumidity();

  // อ่านค่าแรก (ถ้าได้)
  if (!isnan(t) && !isnan(h)) {
    currentT = t;
    currentH = h;
    tempSum += t;
    humidSum += h;
    sampleCount = 1;
    displayCurrentOnLCD(t, h);
  } else {
    displayCurrentOnLCD(NAN, NAN);
  }
  
  lastSampleTime = millis();
}

void loop() {
  checkSerialConnection();

  if (millis() - lastSampleTime >= SAMPLE_INTERVAL_MS) {
    lastSampleTime = millis(); 
    
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    // 1. ถ้าอ่านไม่ได้ ให้ข้ามรอบนี้ (ไม่นับ) -> จอไม่กะพริบ ค่าเฉลี่ยไม่เพี้ยน
    if (isnan(h) || isnan(t)) {
      displayCurrentOnLCD(NAN, NAN); 
      return; 
    }
    
    currentT = t;
    currentH = h;
    displayCurrentOnLCD(t, h);

    // 2. สะสมค่า
    tempSum += t;
    humidSum += h;
    sampleCount++;

    // 3. ครบ 1 ชั่วโมง (1440 ตัวอย่าง)
    if (sampleCount >= SAMPLES_PER_HOUR) {
      
      // [SAFETY GUARD] ป้องกันหารด้วยศูนย์
      if (sampleCount > 0) {
        // [LOGIC] หารด้วย sampleCount เพื่อค่าเฉลี่ยที่ถูกต้องที่สุด
        float avgT = (float)(tempSum / sampleCount);
        float avgH = (float)(humidSum / sampleCount);
        
        if (isLoggingMode) {
          sendToPC(avgT, avgH);
        }
      }

      // [RESET] รีเซ็ตทุกอย่างเริ่มรอบใหม่
      tempSum = 0.0;
      humidSum = 0.0;
      sampleCount = 0;
    }
  }
}