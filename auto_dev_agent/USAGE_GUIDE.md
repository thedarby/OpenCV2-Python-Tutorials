# Auto Dev Agent - คู่มือการใช้งาน

## ภาพรวม
Auto Dev Agent คือระบบพัฒนาซอฟต์แวร์อัตโนมัติที่ช่วยวิเคราะห์ความต้องการ สร้าง workflow ย่อยๆ พัฒนาโค้ด ทดสอบ และปรับปรุงจนได้ผลลัพธ์ที่ต้องการ

## โครงสร้างระบบ

### Components หลัก

1. **Analyzer (analyzer.py)** - วิเคราะห์ความต้องการ
   - แยกย่อย requirement จากคำขอของผู้ใช้
   - ประเมินความซับซ้อนของโปรเจค
   - เสนอเทคโนโลยีที่เหมาะสม

2. **Workflow Generator (workflow_generator.py)** - สร้าง workflow
   - แปลง requirements เป็น task ย่อยๆ
   - กำหนด dependencies ระหว่าง tasks
   - ประมาณการเวลาที่ใช้

3. **Code Generator (code_generator.py)** - สร้างโค้ด
   - เขียนโค้ดตาม workflow
   - สร้าง test files
   - สร้างเอกสาร README

4. **Test Runner (test_runner.py)** - รันการทดสอบ
   - รัน pytest อัตโนมัติ
   - รายงานผลการทดสอบ
   - แสดงรายละเอียด errors

5. **QA Checker (qa_checker.py)** - ตรวจสอบคุณภาพ
   - ตรวจสอบ syntax
   - ตรวจสอบ code style (flake8)
   - ตรวจสอบ security issues

6. **Auto Fixer (auto_fixer.py)** - แก้ไขอัตโนมัติ
   - แก้ไข critical issues
   - แก้ไข style problems
   - พยายาม fix test failures

7. **Main Agent (main.py)** - ประสานงานทั้งหมด
   - รัน workflow แบบ end-to-end
   - แสดง progress และรายงานผล

## การติดตั้ง

```bash
# เข้า directory
cd auto_dev_agent

# ติดตั้ง dependencies
pip install -r requirements.txt
```

## การใช้งาน

### พื้นฐาน
```bash
python main.py "คำอธิบายโปรเจคที่ต้องการ"
```

### ตัวอย่าง
```bash
# สร้างโปรแกรมคำนวณภาษี
python main.py "สร้างโปรแกรมคำนวณภาษีเงินได้ มีฟีเจอร์กรอกข้อมูลรายได้และค่าใช้จ่าย คำนวณภาษีอัตโนมัติตามขั้นบันได แสดงผลลัพธ์เป็นตาราง"

# สร้าง todo app
python main.py "Create a todo list application with database storage"

# พร้อมกำหนด output directory
python main.py "Build a weather API client" --output my_weather_app

# ปิด auto-fix
python main.py "Simple calculator" --no-auto-fix
```

### Options
- `--output, -o`: กำหนด directory สำหรับผลลัพธ์ (default: output)
- `--model, -m`: เลือกโมเดล AI (ยังไม่ได้ใช้งานในเวอร์ชันนี้)
- `--no-auto-fix`: ปิดการแก้ไขอัตโนมัติ
- `--verbose, -v`: แสดงรายละเอียดเพิ่มเติม

## Workflow Process

```
User Request
     ↓
[1] Analyze Requirements
     ↓
[2] Generate Workflow
     ↓
[3] Generate Code
     ↓
[4] Run Tests
     ↓
[5] QA Check
     ↓
[6] Auto Fix (if needed)
     ↓
Re-validate
     ↓
Final Output
```

## โครงสร้างไฟล์ที่สร้าง

เมื่อรันสำเร็จ จะได้ไฟล์ดังนี้:
```
output/
├── main.py           # โปรแกรมหลัก
├── test_main.py      # ไฟล์ทดสอบ
├── README.md         # เอกสารโปรเจค
└── requirements.txt  # Dependencies
```

## การปรับแต่ง

### เพิ่ม Logic ใน Code Generator
แก้ไข `code_generator.py` ในฟังก์ชัน `_generate_main_py()`:

```python
def _generate_main_py(self, workflow, analysis_result) -> str:
    # เพิ่ม logic สำหรับฟีเจอร์ใหม่ๆ
    if 'keyword' in feature.description.lower():
        code += '''
    # Custom feature code here
'''
```

### เพิ่ม Rules ใน Analyzer
แก้ไข `analyzer.py` ในฟังก์ชัน `_extract_requirements()`:

```python
priority_keywords = {
    'high': ['ต้อง', 'จำเป็น', 'สำคัญ'],
    'medium': ['ควร', 'เหมาะสม'],
    'low': ['อาจ', 'ถ้ามีเวลา']
}
```

### เพิ่ม Security Checks
แก้ไข `qa_checker.py` ในฟังก์ชัน `_check_security()`:

```python
security_patterns = [
    ('dangerous_pattern', 'critical', 'Description'),
    # เพิ่ม patterns ใหม่ที่นี่
]
```

## ข้อจำกัด

1. **Template-based Generation**: โค้ดที่สร้างมาจาก template ที่กำหนดไว้
2. **Limited Language Support**: รองรับ Python เป็นหลัก
3. **No AI Model Integration**: ยังไม่ได้เชื่อมต่อกับ AI models จริง
4. **Basic Auto-fix**: แก้ไขได้เฉพาะปัญหาพื้นฐาน

## แนวทางการพัฒนาต่อ

1. **เพิ่ม AI Model Integration**
   - เชื่อมต่อกับ OpenAI API
   - เชื่อมต่อกับ Anthropic API
   - รองรับ Ollama สำหรับ local models

2. **ปรับปรุง Code Generation**
   - ใช้ LLM ในการเขียนโค้ด
   - รองรับ multiple programming languages
   - เพิ่ม code templates มากขึ้น

3. **Enhanced Auto-fix**
   - ใช้ AI ในการวิเคราะห์และแก้ไข
   - รองรับ refactoring ที่ซับซ้อน
   - เพิ่ม intelligent suggestions

4. **Testing Improvements**
   - สร้าง test cases อัตโนมัติด้วย AI
   - เพิ่ม coverage analysis
   - รองรับ integration tests

## Troubleshooting

### ปัญหา: Tests ล้มเหลว
- ตรวจสอบว่า test file ไม่มี syntax errors
- ดูรายละเอียดจาก test report
- ลองรัน manual: `pytest test_main.py -v`

### ปัญหา: QA ไม่ผ่าน
- อ่าน QA report เพื่อหา critical issues
- แก้ไข manually หรือรอให้ auto-fix ทำงาน
- ตรวจสอบ security warnings

### ปัญหา: โค้ดไม่ทำงาน
- ตรวจสอบ dependencies ใน requirements.txt
- รัน `pip install -r requirements.txt`
- ดู error messages จาก console

## License
MIT License
