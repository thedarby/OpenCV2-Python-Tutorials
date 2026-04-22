# Auto Dev Agent - Architecture Documentation

## System Overview

Auto Dev Agent เป็นระบบพัฒนาซอฟต์แวร์อัตโนมัติที่ออกแบบมาให้มี modular architecture ที่สามารถขยายได้ง่าย

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface                          │
│                    (CLI with Rich)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Main Agent                             │
│                   (main.py - Orchestrator)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Coordinates all components in pipeline              │   │
│  │  Manages state and progress tracking                 │   │
│  │  Handles error recovery and retry logic              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Analyzer    │    │   Workflow    │    │    Code       │
│               │    │  Generator    │    │  Generator    │
│ • Parse reqs  │    │ • Create tasks│    │ • Write code  │
│ • Classify    │    │ • Set deps    │    │ • Gen tests   │
│ • Prioritize  │    │ • Estimate    │    │ • Gen docs    │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Quality Assurance Loop                    │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │ Test Runner │ → │ QA Checker  │ → │ Auto Fixer  │       │
│  │             │   │             │   │             │       │
│  │ • Run pytest│   │ • Syntax    │   │ • Fix crit  │       │
│  │ • Parse res │   │ • Style     │   │ • Fix style │       │
│  │ • Report    │   │ • Security  │   │ • Retry     │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Output Layer                           │
│              (Generated Project Files)                      │
│  • main.py  • test_main.py  • README.md  • requirements.txt│
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Analyzer (`analyzer.py`)

**Responsibility**: วิเคราะห์และแยกย่อยความต้องการ

**Key Classes**:
- `Requirement`: Data model สำหรับ requirement แต่ละข้อ
- `AnalysisResult`: ผลลัพธ์การวิเคราะห์ทั้งหมด
- `RequirementAnalyzer`: Logic หลักในการวิเคราะห์

**Process Flow**:
```
User Input → Text Splitting → Keyword Matching → 
Classification → Prioritization → Technology Suggestion → Output
```

**Extensibility Points**:
- เพิ่ม keywords ใน `priority_keywords` และ `category_keywords`
- ปรับปรุง `_suggest_technologies()` สำหรับ tech stack ใหม่
- เพิ่ม NLP/ML model สำหรับการวิเคราะห์ที่ฉลาดขึ้น

### 2. Workflow Generator (`workflow_generator.py`)

**Responsibility**: สร้าง workflow จาก requirements

**Key Classes**:
- `WorkflowTask`: Task แต่ละงานใน workflow
- `Workflow`: collection ของ tasks ทั้งหมด
- `WorkflowGenerator`: Logic ในการสร้าง workflow

**Process Flow**:
```
Analysis Result → Group by Category → Create Tasks → 
Set Dependencies → Estimate Time → Output Workflow
```

**Task Categories**:
1. Project Setup
2. Feature Implementation
3. Testing
4. QA Check
5. Documentation

### 3. Code Generator (`code_generator.py`)

**Responsibility**: สร้าง source code จาก workflow

**Key Classes**:
- `GeneratedFile`: ไฟล์โค้ดที่สร้าง
- `CodeGenerationResult`: ผลลัพธ์การสร้างโค้ดทั้งหมด
- `CodeGenerator`: Logic ในการ generate code

**Template System**:
- ใช้ string templates สำหรับ code patterns ต่างๆ
- สามารถเพิ่ม template ใหม่ได้ตามต้องการ
- รองรับ multiple file generation

**Generated Files**:
- `main.py`: โปรแกรมหลักพร้อม business logic
- `test_main.py`: Unit tests
- `README.md`: Documentation
- `requirements.txt`: Dependencies

### 4. Test Runner (`test_runner.py`)

**Responsibility**: รันและรายงานผลการทดสอบ

**Key Classes**:
- `TestResult`: ผลลัพธ์การทดสอบแต่ละ test
- `TestReport`: รายงานสรุปทั้งหมด
- `TestRunner`: Logic ในการรัน tests

**Features**:
- รัน pytest อัตโนมัติ
- Parse output เพื่อแสดงผล
- คำนวณ success rate
- แสดง detailed error messages

### 5. QA Checker (`qa_checker.py`)

**Responsibility**: ตรวจสอบคุณภาพโค้ด

**Key Classes**:
- `QAIssue`: ปัญหาที่พบ
- `QAReport`: รายงาน QA ทั้งหมด
- `QAChecker`: Logic ในการตรวจสอบ

**Check Categories**:
1. **Syntax Check**: Compile Python code
2. **Style Check**: flake8 integration
3. **Import Check**: Unused imports detection
4. **Security Check**: Dangerous patterns detection

**Severity Levels**:
- `critical`: ต้องแก้ไขทันที (syntax errors, security issues)
- `warning`: ควรแก้ไข (style violations)
- `info`: แนะนำ (best practices)

### 6. Auto Fixer (`auto_fixer.py`)

**Responsibility**: แก้ไขปัญหาโดยอัตโนมัติ

**Key Classes**:
- `FixAction`: การแก้ไขที่จะทำ
- `FixReport`: รายงานการแก้ไข
- `AutoFixer`: Logic ในการแก้ไข

**Fix Strategies**:
1. **Replace**: แทนที่ code ที่มีปัญหา
2. **Insert**: เพิ่ม code ใหม่
3. **Delete**: ลบหรือ comment out
4. **Reformat**: จัดรูปแบบใหม่

**Limitations**:
- แก้ไขได้เฉพาะ patterns ที่รู้จัก
- ไม่สามารถเข้าใจ context ที่ซับซ้อนได้
- ต้องการ human review สำหรับ critical changes

### 7. Main Agent (`main.py`)

**Responsibility**: ประสานงานทุก components

**Key Classes**:
- `AutoDevAgent`: Main orchestrator class

**Pipeline Execution**:
```
1. Analyze Requirements
2. Generate Workflow
3. Generate Code
4. Run Tests
5. QA Check
6. Auto Fix (if needed)
7. Re-validate
8. Final Report
```

**Error Handling**:
- Try-catch blocks ในแต่ละ step
- Graceful degradation
- Detailed error reporting

## Data Flow

```
User Request (string)
    │
    ▼
┌─────────────────────────────────┐
│ RequirementAnalyzer.analyze()   │
│ Input: string                   │
│ Output: AnalysisResult          │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ WorkflowGenerator.generate()    │
│ Input: AnalysisResult           │
│ Output: Workflow                │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ CodeGenerator.generate()        │
│ Input: Workflow, AnalysisResult │
│ Output: CodeGenerationResult    │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ TestRunner.run_tests()          │
│ Input: test file path           │
│ Output: TestReport              │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ QAChecker.check()               │
│ Input: list of files            │
│ Output: QAReport                │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ AutoFixer.fix()                 │
│ Input: QAReport, TestReport     │
│ Output: FixReport               │
└─────────────────────────────────┘
```

## Extension Points

### Adding New AI Models

```python
# In analyzer.py
class RequirementAnalyzer:
    def __init__(self, model_client=None):
        self.model_client = model_client  # Inject AI client
    
    def analyze_with_ai(self, user_request: str):
        # Use OpenAI, Anthropic, or local model
        response = self.model_client.generate(...)
        return self._parse_ai_response(response)
```

### Adding New Code Templates

```python
# In code_generator.py
def _generate_main_py(self, workflow, analysis_result):
    # Add new template
    if self._is_web_app(analysis_result):
        return self._generate_web_app_template(...)
    elif self._is_cli_app(analysis_result):
        return self._generate_cli_app_template(...)
```

### Adding New QA Checks

```python
# In qa_checker.py
def _check_performance(self, files):
    issues = []
    for file in files:
        # Add performance checks
        pass
    return issues

def check(self, files=None):
    # ... existing code ...
    perf_issues = self._check_performance(files)
    all_issues.extend(perf_issues)
```

## Configuration System (Future)

```yaml
# config.yaml
model:
  provider: openai  # or anthropic, ollama
  name: gpt-4
  
generation:
  language: python
  include_tests: true
  include_docs: true
  
qa:
  run_tests: true
  run_linters: true
  auto_fix: true
  
output:
  directory: ./output
  format: project
```

## Testing Strategy

### Unit Tests
- ทดสอบแต่ละ module แยกกัน
- Mock dependencies
- Verify expected outputs

### Integration Tests
- ทดสอบ pipeline ทั้งหมด
- Verify end-to-end flow
- Check file generation

### Example Test Structure
```
tests/
├── test_analyzer.py
├── test_workflow_generator.py
├── test_code_generator.py
├── test_test_runner.py
├── test_qa_checker.py
├── test_auto_fixer.py
└── test_integration.py
```

## Performance Considerations

1. **Parallel Processing**: รัน tests และ QA checks แบบ parallel
2. **Caching**: Cache analysis results สำหรับ repeated runs
3. **Incremental Generation**: Generate only changed files
4. **Streaming Output**: แสดงผลแบบ real-time

## Security Considerations

1. **Input Validation**: Validate user requests
2. **Code Sanitization**: Check generated code for security issues
3. **Sandboxing**: Run generated code in isolated environment
4. **Dependency Scanning**: Scan for vulnerable packages

## Future Enhancements

1. **AI Integration**: Connect to LLM APIs
2. **Multi-language Support**: Generate code in multiple languages
3. **GUI Interface**: Web-based UI
4. **Plugin System**: Extensible plugin architecture
5. **Project Templates**: Pre-built templates for common projects
6. **Database Support**: Auto-generate database schemas
7. **API Generation**: Auto-generate REST/GraphQL APIs
8. **Deployment Scripts**: Generate Docker, CI/CD configs
