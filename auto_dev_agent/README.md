# Auto Dev Agent - ระบบพัฒนาซอฟต์แวร์อัตโนมัติ

## ภาพรวม
ระบบที่ช่วยวิเคราะห์ความต้องการ (Requirements), สร้าง workflow ย่อยๆ, พัฒนาโค้ด, ทดสอบ, และปรับปรุงจนได้ผลลัพธ์ที่ต้องการ

## โครงสร้างระบบ

### 1. Core Components
- **Requirement Analyzer**: วิเคราะห์และแยกย่อยความต้องการ
- **Workflow Generator**: สร้าง workflow ย่อยๆ จากความต้องการ
- **Code Generator**: เขียนโค้ดตาม workflow
- **Test Runner**: รันการทดสอบอัตโนมัติ
- **QA Checker**: ตรวจสอบคุณภาพโค้ด
- **Auto Fixer**: แก้ไขข้อผิดพลาดโดยอัตโนมัติ

### 2. Workflow Process
```
User Request → Requirement Analysis → Workflow Generation → 
Implementation → Testing → QA Check → Auto Fix (if needed) → Final Output
```

## การติดตั้งและการใช้งาน

### ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### รันโปรแกรม
```bash
python main.py "คำอธิบายโปรเจคที่ต้องการ"
```

## ตัวอย่างการใช้งาน
```bash
python main.py "สร้างโปรแกรมคำนวณภาษีที่มี UI อย่างง่าย"
```

## โครงสร้างไฟล์
- `main.py`: โปรแกรมหลัก
- `analyzer.py`: วิเคราะห์ความต้องการ
- `workflow_generator.py`: สร้าง workflow
- `code_generator.py`: สร้างโค้ด
- `test_runner.py`: รันการทดสอบ
- `qa_checker.py`: ตรวจสอบคุณภาพ
- `auto_fixer.py`: แก้ไขข้อผิดพลาด
- `requirements.txt`: Dependencies
- `README.md`: คู่มือการใช้งาน
