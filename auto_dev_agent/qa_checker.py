"""
QA Checker - ตรวจสอบคุณภาพโค้ด
"""
import subprocess
import sys
import os
from typing import List, Dict, Any
from pydantic import BaseModel

class QAIssue(BaseModel):
    severity: str  # critical, warning, info
    category: str  # syntax, style, security, performance
    message: str
    file: str
    line: int = 0

class QAReport(BaseModel):
    total_issues: int
    critical: int
    warnings: int
    info: int
    issues: List[QAIssue]
    passed: bool

class QAChecker:
    def __init__(self):
        self.issues = []
    
    def check(self, files: List[str] = None) -> QAReport:
        """ตรวจสอบคุณภาพโค้ด"""
        
        print(f"\n{'='*60}")
        print("QA CHECK - Code Quality Analysis")
        print(f"{'='*60}\n")
        
        if files is None:
            # หาไฟล์ Python ทั้งหมดใน directory
            files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'qa_checker.py']
        
        all_issues = []
        
        # 1. Syntax Check
        print("🔍 Checking syntax...")
        syntax_issues = self._check_syntax(files)
        all_issues.extend(syntax_issues)
        print(f"   Found {len(syntax_issues)} syntax issues")
        
        # 2. Style Check (flake8)
        print("🎨 Checking code style...")
        style_issues = self._check_style(files)
        all_issues.extend(style_issues)
        print(f"   Found {len(style_issues)} style issues")
        
        # 3. Import Check
        print("📦 Checking imports...")
        import_issues = self._check_imports(files)
        all_issues.extend(import_issues)
        print(f"   Found {len(import_issues)} import issues")
        
        # 4. Basic Security Check
        print("🔒 Checking for common security issues...")
        security_issues = self._check_security(files)
        all_issues.extend(security_issues)
        print(f"   Found {len(security_issues)} security issues")
        
        # สร้างรายงาน
        critical_count = sum(1 for i in all_issues if i.severity == 'critical')
        warning_count = sum(1 for i in all_issues if i.severity == 'warning')
        info_count = sum(1 for i in all_issues if i.severity == 'info')
        
        report = QAReport(
            total_issues=len(all_issues),
            critical=critical_count,
            warnings=warning_count,
            info=info_count,
            issues=all_issues,
            passed=(critical_count == 0)
        )
        
        self._print_report(report)
        
        return report
    
    def _check_syntax(self, files: List[str]) -> List[QAIssue]:
        """ตรวจสอบ syntax"""
        issues = []
        
        for file in files:
            if not os.path.exists(file):
                continue
            
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    source = f.read()
                compile(source, file, 'exec')
            except SyntaxError as e:
                issues.append(QAIssue(
                    severity='critical',
                    category='syntax',
                    message=f"Syntax error: {e.msg}",
                    file=file,
                    line=e.lineno or 0
                ))
            except Exception as e:
                issues.append(QAIssue(
                    severity='warning',
                    category='syntax',
                    message=f"Could not parse file: {str(e)}",
                    file=file,
                    line=0
                ))
        
        return issues
    
    def _check_style(self, files: List[str]) -> List[QAIssue]:
        """ตรวจสอบ code style ด้วย flake8"""
        issues = []
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "flake8", "--max-line-length=120"] + files,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if ':' in line:
                        parts = line.split(':')
                        if len(parts) >= 3:
                            file = parts[0]
                            try:
                                line_num = int(parts[1])
                            except:
                                line_num = 0
                            message = ':'.join(parts[2:]).strip()
                            
                            # กำหนด severity ตาม type ของ error
                            severity = 'info'
                            if 'E9' in message or 'F6' in message:  # syntax errors
                                severity = 'critical'
                            elif 'W' in message:  # warnings
                                severity = 'warning'
                            
                            issues.append(QAIssue(
                                severity=severity,
                                category='style',
                                message=message,
                                file=file,
                                line=line_num
                            ))
        except subprocess.TimeoutExpired:
            issues.append(QAIssue(
                severity='info',
                category='style',
                message="Style check timed out",
                file="*",
                line=0
            ))
        except FileNotFoundError:
            issues.append(QAIssue(
                severity='info',
                category='style',
                message="flake8 not installed, skipping style check",
                file="*",
                line=0
            ))
        except Exception as e:
            issues.append(QAIssue(
                severity='info',
                category='style',
                message=f"Style check error: {str(e)}",
                file="*",
                line=0
            ))
        
        return issues
    
    def _check_imports(self, files: List[str]) -> List[QAIssue]:
        """ตรวจสอบ imports"""
        issues = []
        
        for file in files:
            if not os.path.exists(file):
                continue
            
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                for i, line in enumerate(lines, 1):
                    # ตรวจสอบ unused imports (แบบง่าย)
                    if 'import' in line and not line.strip().startswith('#'):
                        # TODO: Implement more sophisticated import checking
                        pass
                        
            except Exception as e:
                issues.append(QAIssue(
                    severity='warning',
                    category='style',
                    message=f"Could not check imports: {str(e)}",
                    file=file,
                    line=0
                ))
        
        return issues
    
    def _check_security(self, files: List[str]) -> List[QAIssue]:
        """ตรวจสอบ security issues แบบพื้นฐาน"""
        issues = []
        
        security_patterns = [
            ('eval(', 'critical', 'Use of eval() can be dangerous'),
            ('exec(', 'critical', 'Use of exec() can be dangerous'),
            ('__import__', 'warning', 'Dynamic importing detected'),
            ('os.system(', 'warning', 'Consider using subprocess instead'),
            ('input(', 'info', 'Ensure input is properly validated'),
        ]
        
        for file in files:
            if not os.path.exists(file):
                continue
            
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                for i, line in enumerate(lines, 1):
                    # ข้าม comment
                    if line.strip().startswith('#'):
                        continue
                    
                    for pattern, severity, message in security_patterns:
                        if pattern in line:
                            issues.append(QAIssue(
                                severity=severity,
                                category='security',
                                message=f"{message}: {pattern}",
                                file=file,
                                line=i
                            ))
                            
            except Exception as e:
                issues.append(QAIssue(
                    severity='warning',
                    category='security',
                    message=f"Could not check security: {str(e)}",
                    file=file,
                    line=0
                ))
        
        return issues
    
    def _print_report(self, report: QAReport):
        """แสดงรายงาน QA"""
        
        print(f"\n{'='*60}")
        print("QA REPORT")
        print(f"{'='*60}")
        
        status = "✅ PASSED" if report.passed else "❌ FAILED"
        print(f"Status: {status}")
        print(f"Total Issues: {report.total_issues}")
        print(f"🔴 Critical: {report.critical}")
        print(f"🟡 Warnings: {report.warnings}")
        print(f"🔵 Info: {report.info}")
        print(f"{'='*60}\n")
        
        if report.issues:
            print("Issues:")
            
            # แสดง critical ก่อน
            critical_issues = [i for i in report.issues if i.severity == 'critical']
            if critical_issues:
                print("\n🔴 Critical Issues:")
                for issue in critical_issues:
                    print(f"  • {issue.file}:{issue.line} - {issue.message}")
            
            # แสดง warnings
            warning_issues = [i for i in report.issues if i.severity == 'warning']
            if warning_issues:
                print("\n🟡 Warnings:")
                for issue in warning_issues[:10]:  # แสดงแค่ 10 อันแรก
                    print(f"  • {issue.file}:{issue.line} - {issue.message}")
                if len(warning_issues) > 10:
                    print(f"  ... and {len(warning_issues) - 10} more warnings")
            
            # แสดง info
            info_issues = [i for i in report.issues if i.severity == 'info']
            if info_issues:
                print("\n🔵 Info:")
                for issue in info_issues[:5]:  # แสดงแค่ 5 อันแรก
                    print(f"  • {issue.file}:{issue.line} - {issue.message}")
                if len(info_issues) > 5:
                    print(f"  ... and {len(info_issues) - 5} more info items")
            
            print()


if __name__ == "__main__":
    # ทดสอบ QA checker
    checker = QAChecker()
    
    # สร้างไฟล์ทดสอบที่มีปัญหา
    test_code = '''
# Test file with some issues
import os
import sys

def dangerous_function():
    user_input = input("Enter code: ")
    eval(user_input)  # Dangerous!

def good_function():
    x = 10
    y = 20
    return x + y
'''
    
    with open("test_qa.py", "w") as f:
        f.write(test_code)
    
    # รัน QA check
    report = checker.check(["test_qa.py"])
    
    print(f"\nFinal Result: {'PASSED' if report.passed else 'NEEDS FIXES'}")
    
    # ลบไฟล์ทดสอบ
    os.remove("test_qa.py")
