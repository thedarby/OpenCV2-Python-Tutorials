"""
Code Generator - สร้างโค้ดตาม workflow และ requirements
"""
from typing import List, Dict, Any
from pydantic import BaseModel
import os
import json

class GeneratedFile(BaseModel):
    filename: str
    content: str
    language: str
    description: str

class CodeGenerationResult(BaseModel):
    files: List[GeneratedFile]
    setup_instructions: str
    run_instructions: str

class CodeGenerator:
    def __init__(self, model_client=None):
        self.model_client = model_client
        self.generated_files = []
    
    def generate(self, workflow, analysis_result) -> CodeGenerationResult:
        """สร้างโค้ดจาก workflow และ requirements"""
        
        files = []
        
        # 1. สร้าง main.py
        main_content = self._generate_main_py(workflow, analysis_result)
        files.append(GeneratedFile(
            filename="main.py",
            content=main_content,
            language="python",
            description="โปรแกรมหลัก"
        ))
        
        # 2. สร้าง test file
        test_content = self._generate_test_py(workflow, analysis_result)
        files.append(GeneratedFile(
            filename="test_main.py",
            content=test_content,
            language="python",
            description="ไฟล์ทดสอบ"
        ))
        
        # 3. สร้าง README
        readme_content = self._generate_readme(workflow, analysis_result)
        files.append(GeneratedFile(
            filename="README.md",
            content=readme_content,
            language="markdown",
            description="เอกสารโปรเจค"
        ))
        
        # 4. สร้าง requirements.txt ถ้ายังไม่มี
        if not os.path.exists("requirements.txt"):
            req_content = self._generate_requirements(analysis_result)
            files.append(GeneratedFile(
                filename="requirements.txt",
                content=req_content,
                language="text",
                description="Dependencies"
            ))
        
        return CodeGenerationResult(
            files=files,
            setup_instructions="pip install -r requirements.txt",
            run_instructions="python main.py"
        )
    
    def _generate_main_py(self, workflow, analysis_result) -> str:
        """สร้างไฟล์ main.py"""
        
        # วิเคราะห์ว่าต้องสร้างฟีเจอร์อะไรบ้าง
        features = [req for req in analysis_result.requirements 
                   if req.category == 'feature']
        
        code = '''"""
Auto-generated main program
"""
'''
        
        # เพิ่ม imports ตามความเหมาะสม
        if any('tax' in req.description.lower() or 'คำนวณ' in req.description for req in features):
            code += '''from typing import Dict, List
import json

'''
        
        code += '''
def main():
    """Main function"""
    print("Welcome to the Auto-Generated Application!")
    print("=" * 50)
    
'''
        
        # เพิ่ม logic สำหรับแต่ละ feature
        for i, feature in enumerate(features, 1):
            desc_lower = feature.description.lower()
            
            if 'tax' in desc_lower or 'ภาษี' in desc_lower or 'คำนวณ' in desc_lower:
                code += f'''    # Feature {i}: {feature.description}
    print("\\nFeature {i}: Tax Calculator")
    result = calculate_tax()
    print(f"Result: {{result}}")
    
'''
            elif 'input' in desc_lower or 'กรอก' in desc_lower or 'data' in desc_lower:
                code += f'''    # Feature {i}: {feature.description}
    print("\\nFeature {i}: Data Input")
    data = get_user_input()
    print(f"Received data: {{data}}")
    
'''
            elif 'table' in desc_lower or 'ตาราง' in desc_lower or 'display' in desc_lower:
                code += f'''    # Feature {i}: {feature.description}
    print("\\nFeature {i}: Display Table")
    display_table()
    
'''
            else:
                code += f'''    # Feature {i}: {feature.description}
    print("\\nFeature {i}: Custom Feature")
    custom_feature()
    
'''
        
        code += '''    print("\\n" + "=" * 50)
    print("Application completed successfully!")


'''
        
        # เพิ่ม helper functions
        code += '''def calculate_tax():
    """Calculate tax based on income"""
    # TODO: Implement tax calculation logic
    income = float(input("Enter income: "))
    deductions = float(input("Enter deductions: "))
    
    taxable_income = income - deductions
    
    # Simple tax brackets (example)
    if taxable_income <= 0:
        tax = 0
    elif taxable_income <= 150000:
        tax = 0
    elif taxable_income <= 300000:
        tax = (taxable_income - 150000) * 0.05
    elif taxable_income <= 500000:
        tax = 7500 + (taxable_income - 300000) * 0.10
    else:
        tax = 27500 + (taxable_income - 500000) * 0.15
    
    return {
        "taxable_income": taxable_income,
        "tax": tax,
        "effective_rate": (tax / taxable_income * 100) if taxable_income > 0 else 0
    }


def get_user_input():
    """Get input from user"""
    data = {}
    print("Enter your information:")
    data["name"] = input("Name: ")
    data["age"] = input("Age: ")
    data["email"] = input("Email: ")
    return data


def display_table():
    """Display data in table format"""
    headers = ["ID", "Name", "Value"]
    rows = [
        [1, "Item A", 100],
        [2, "Item B", 200],
        [3, "Item C", 300]
    ]
    
    # Print header
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join(["-" * (len(h) + 2) for h in headers]) + "|")
    
    # Print rows
    for row in rows:
        print("| " + " | ".join(str(x) for x in row) + " |")


def custom_feature():
    """Custom feature placeholder"""
    print("Custom feature executed")


if __name__ == "__main__":
    main()
'''
        
        return code
    
    def _generate_test_py(self, workflow, analysis_result) -> str:
        """สร้างไฟล์ test"""
        
        code = '''"""
Auto-generated test file
"""
import pytest


def test_calculate_tax_zero_income():
    """Test tax calculation with zero income"""
    taxable_income = 0
    expected_tax = 0
    
    # Simple assertion
    assert taxable_income <= 0


def test_calculate_tax_low_income():
    """Test tax calculation with low income"""
    taxable_income = 100000
    expected_tax = 0  # Below threshold
    
    assert taxable_income <= 150000


def test_calculate_tax_medium_income():
    """Test tax calculation with medium income"""
    taxable_income = 200000
    
    assert taxable_income > 150000
    assert taxable_income <= 300000


def test_display_table_format():
    """Test table display format"""
    headers = ["ID", "Name", "Value"]
    assert len(headers) == 3
    assert all(isinstance(h, str) for h in headers)


def test_user_input_validation():
    """Test user input validation"""
    test_data = {"name": "Test", "age": "25", "email": "test@example.com"}
    
    assert "name" in test_data
    assert "email" in test_data
    assert "@" in test_data["email"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
        
        return code
    
    def _generate_readme(self, workflow, analysis_result) -> str:
        """สร้างไฟล์ README"""
        
        readme = f"""# Auto-Generated Project

## Description
{analysis_result.original_request}

## Features
"""
        
        for req in analysis_result.requirements:
            if req.category == 'feature':
                readme += f"- {req.description}\n"
        
        readme += f"""
## Technologies
{', '.join(analysis_result.suggested_technologies)}

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Testing

```bash
pytest test_main.py -v
```

## Project Structure

- `main.py` - Main application
- `test_main.py` - Test suite
- `requirements.txt` - Dependencies
- `README.md` - This file

## Workflow

Total Estimated Time: {workflow.total_estimated_time} minutes

### Tasks
"""
        
        for task in workflow.tasks:
            status_icon = "✅" if task.status == "completed" else "⏳"
            readme += f"{status_icon} **{task.name}**: {task.description}\n"
        
        readme += """
## License
MIT License
"""
        
        return readme
    
    def _generate_requirements(self, analysis_result) -> str:
        """สร้างไฟล์ requirements.txt"""
        
        reqs = ["pytest>=7.4.0"]
        
        # เพิ่ม dependencies ตาม technologies ที่แนะนำ
        for tech in analysis_result.suggested_technologies:
            if 'FastAPI' in tech:
                reqs.append("fastapi>=0.100.0")
                reqs.append("uvicorn>=0.23.0")
            elif 'React' in tech or 'Vue' in tech:
                reqs.append("# Frontend framework needed separately")
            elif 'Tkinter' in tech or 'PyQt' in tech:
                reqs.append("# GUI libraries (usually included with Python)")
        
        return "\n".join(reqs)
    
    def save_files(self, result: CodeGenerationResult, output_dir: str = "."):
        """บันทึกไฟล์ที่สร้าง"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        for file in result.files:
            filepath = os.path.join(output_dir, file.filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(file.content)
            print(f"✓ Created: {file.filename}")
        
        return result.files


if __name__ == "__main__":
    # ทดสอบ code generator
    from analyzer import RequirementAnalyzer
    from workflow_generator import WorkflowGenerator
    
    analyzer = RequirementAnalyzer()
    test_request = """
    ฉันต้องการสร้างโปรแกรมคำนวณภาษีเงินได้
    ต้องมีฟีเจอร์กรอกข้อมูลรายได้และค่าใช้จ่าย
    ควรคำนวณภาษีอัตโนมัติตามขั้นบันได
    ต้องแสดงผลลัพธ์เป็นตาราง
    """
    
    analysis_result = analyzer.analyze(test_request)
    
    workflow_gen = WorkflowGenerator()
    workflow = workflow_gen.generate(analysis_result)
    
    code_gen = CodeGenerator()
    result = code_gen.generate(workflow, analysis_result)
    
    print(f"\nGenerated {len(result.files)} files:")
    for file in result.files:
        print(f"  - {file.filename} ({file.language})")
    
    print(f"\nSetup: {result.setup_instructions}")
    print(f"Run: {result.run_instructions}")
