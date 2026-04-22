"""
Test Runner - รันการทดสอบอัตโนมัติ
"""
import subprocess
import sys
import os
from typing import List, Dict, Any
from pydantic import BaseModel

class TestResult(BaseModel):
    test_name: str
    passed: bool
    error_message: str = ""
    execution_time: float = 0.0

class TestReport(BaseModel):
    total_tests: int
    passed: int
    failed: int
    results: List[TestResult]
    success_rate: float

class TestRunner:
    def __init__(self):
        self.results = []
    
    def run_tests(self, test_file: str = "test_main.py") -> TestReport:
        """รันการทดสอบทั้งหมด"""
        
        print(f"\n{'='*60}")
        print(f"RUNNING TESTS: {test_file}")
        print(f"{'='*60}\n")
        
        results = []
        
        # ตรวจสอบว่ามีไฟล์ทดสอบหรือไม่
        if not os.path.exists(test_file):
            print(f"⚠️  Test file not found: {test_file}")
            return TestReport(
                total_tests=0,
                passed=0,
                failed=0,
                results=[],
                success_rate=0.0
            )
        
        # รัน pytest
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            output = result.stdout + result.stderr
            
            # Parse ผลลัพธ์
            lines = output.split('\n')
            current_test = None
            
            for line in lines:
                if 'test_' in line and ('PASSED' in line or 'FAILED' in line or 'ERROR' in line):
                    parts = line.split()
                    if len(parts) >= 2:
                        test_name = parts[0]
                        passed = 'PASSED' in line
                        error_msg = ""
                        
                        if not passed:
                            # หา error message
                            error_start = line.find('FAILED')
                            if error_start != -1:
                                error_msg = line[error_start:]
                        
                        results.append(TestResult(
                            test_name=test_name,
                            passed=passed,
                            error_message=error_msg
                        ))
            
            # ถ้า parse ไม่ได้ว่า ให้ดูจาก summary
            if not results:
                if 'passed' in output:
                    # สร้าง result แบบง่าย
                    results.append(TestResult(
                        test_name="all_tests",
                        passed=result.returncode == 0,
                        error_message="" if result.returncode == 0 else output[-500:]
                    ))
            
            passed_count = sum(1 for r in results if r.passed)
            failed_count = len(results) - passed_count
            
            report = TestReport(
                total_tests=len(results),
                passed=passed_count,
                failed=failed_count,
                results=results,
                success_rate=(passed_count / len(results) * 100) if results else 0.0
            )
            
            self._print_report(report)
            
            return report
            
        except subprocess.TimeoutExpired:
            print("❌ Tests timed out")
            return TestReport(
                total_tests=0,
                passed=0,
                failed=0,
                results=[],
                success_rate=0.0
            )
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return TestReport(
                total_tests=0,
                passed=0,
                failed=0,
                results=[],
                success_rate=0.0
            )
    
    def _print_report(self, report: TestReport):
        """แสดงรายงานผลการทดสอบ"""
        
        print(f"\n{'='*60}")
        print("TEST REPORT")
        print(f"{'='*60}")
        print(f"Total Tests: {report.total_tests}")
        print(f"✅ Passed: {report.passed}")
        print(f"❌ Failed: {report.failed}")
        print(f"📊 Success Rate: {report.success_rate:.1f}%")
        print(f"{'='*60}\n")
        
        if report.results:
            print("Detailed Results:")
            for result in report.results:
                icon = "✅" if result.passed else "❌"
                print(f"  {icon} {result.test_name}")
                if not result.passed and result.error_message:
                    print(f"      Error: {result.error_message[:100]}...")
            print()
    
    def run_specific_test(self, test_file: str, test_name: str) -> TestResult:
        """รันการทดสอบเฉพาะชื่อ"""
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", f"{test_file}::{test_name}", "-v"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            passed = result.returncode == 0
            
            return TestResult(
                test_name=test_name,
                passed=passed,
                error_message="" if passed else result.stderr[-200:]
            )
            
        except Exception as e:
            return TestResult(
                test_name=test_name,
                passed=False,
                error_message=str(e)
            )


if __name__ == "__main__":
    # ทดสอบ test runner
    runner = TestRunner()
    
    # สร้างไฟล์ทดสอบตัวอย่าง
    test_content = '''
def test_simple_addition():
    assert 1 + 1 == 2

def test_string_concatenation():
    assert "hello" + " " + "world" == "hello world"

def test_list_length():
    assert len([1, 2, 3]) == 3
'''
    
    with open("test_example.py", "w") as f:
        f.write(test_content)
    
    # รันการทดสอบ
    report = runner.run_tests("test_example.py")
    
    print(f"\nFinal Result: {'SUCCESS' if report.failed == 0 else 'FAILURE'}")
    
    # ลบไฟล์ทดสอบ
    os.remove("test_example.py")
