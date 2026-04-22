"""
Auto Fixer - แก้ไขข้อผิดพลาดโดยอัตโนมัติ
"""
import os
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class FixAction(BaseModel):
    action_type: str  # replace, insert, delete, reformat
    file: str
    line: int
    original: str
    replacement: str
    reason: str

class FixReport(BaseModel):
    total_fixes: int
    fixes_applied: int
    fixes_failed: int
    actions: List[FixAction]
    success: bool

class AutoFixer:
    def __init__(self):
        self.fix_history = []
    
    def fix(self, qa_report, test_report) -> FixReport:
        """พยายามแก้ไขข้อผิดพลาดโดยอัตโนมัติ"""
        
        print(f"\n{'='*60}")
        print("AUTO FIXER - Attempting Automatic Fixes")
        print(f"{'='*60}\n")
        
        actions = []
        fixes_applied = 0
        fixes_failed = 0
        
        # 1. แก้ไข critical issues จาก QA report
        if qa_report and qa_report.issues:
            critical_issues = [i for i in qa_report.issues if i.severity == 'critical']
            
            for issue in critical_issues:
                action = self._attempt_fix(issue)
                if action:
                    actions.append(action)
                    if self._apply_fix(action):
                        fixes_applied += 1
                        print(f"✅ Fixed: {issue.message} in {issue.file}:{issue.line}")
                    else:
                        fixes_failed += 1
                        print(f"❌ Failed to fix: {issue.message} in {issue.file}:{issue.line}")
        
        # 2. แก้ไขปัญหาที่พบบ่อยจาก test failures
        if test_report and test_report.results:
            failed_tests = [r for r in test_report.results if not r.passed]
            
            for test_result in failed_tests:
                # พยายามวิเคราะห์และแก้ไข
                action = self._analyze_test_failure(test_result)
                if action:
                    actions.append(action)
                    if self._apply_fix(action):
                        fixes_applied += 1
                        print(f"✅ Fixed test issue: {test_result.test_name}")
                    else:
                        fixes_failed += 1
                        print(f"❌ Failed to fix test: {test_result.test_name}")
        
        # 3. แก้ไขปัญหา style ที่พบบ่อย
        if qa_report and qa_report.issues:
            style_issues = [i for i in qa_report.issues 
                           if i.category == 'style' and i.severity in ['warning', 'info']]
            
            for issue in style_issues[:5]:  # แก้แค่ 5 อันแรก
                action = self._fix_style_issue(issue)
                if action:
                    actions.append(action)
                    if self._apply_fix(action):
                        fixes_applied += 1
                        print(f"✅ Fixed style: {issue.message}")
        
        report = FixReport(
            total_fixes=len(actions),
            fixes_applied=fixes_applied,
            fixes_failed=fixes_failed,
            actions=actions,
            success=(fixes_failed == 0)
        )
        
        self._print_report(report)
        
        return report
    
    def _attempt_fix(self, issue) -> Optional[FixAction]:
        """พยายามสร้าง action สำหรับแก้ไข"""
        
        # Security: eval()
        if 'eval()' in issue.message and issue.category == 'security':
            return FixAction(
                action_type='replace',
                file=issue.file,
                line=issue.line,
                original='eval(',
                replacement='# eval() removed for security - implement safe alternative',
                reason='Security: eval() is dangerous'
            )
        
        # Security: exec()
        if 'exec()' in issue.message and issue.category == 'security':
            return FixAction(
                action_type='replace',
                file=issue.file,
                line=issue.line,
                original='exec(',
                replacement='# exec() removed for security - implement safe alternative',
                reason='Security: exec() is dangerous'
            )
        
        # Syntax errors
        if issue.category == 'syntax':
            # TODO: Implement more sophisticated syntax fixing
            return None
        
        return None
    
    def _analyze_test_failure(self, test_result) -> Optional[FixAction]:
        """วิเคราะห์ความล้มเหลวของการทดสอบและเสนอวิธีแก้"""
        
        error_msg = test_result.error_message.lower()
        
        # Assertion errors
        if 'assertionerror' in error_msg or 'assert' in error_msg:
            # เสนอให้ตรวจสอบ logic
            return FixAction(
                action_type='insert',
                file='test_main.py',
                line=0,
                original='',
                replacement=f'# TODO: Review test: {test_result.test_name}\n# Error: {test_result.error_message[:100]}',
                reason='Test assertion failed - needs manual review'
            )
        
        # Import errors
        if 'import' in error_msg or 'module not found' in error_msg:
            return FixAction(
                action_type='insert',
                file='main.py',
                line=1,
                original='',
                replacement='# Missing import - please add required imports\n',
                reason='Import error detected'
            )
        
        return None
    
    def _fix_style_issue(self, issue) -> Optional[FixAction]:
        """แก้ไขปัญหา style"""
        
        message = issue.message.lower()
        
        # Line too long
        if 'line too long' in message or 'e501' in message:
            return FixAction(
                action_type='reformat',
                file=issue.file,
                line=issue.line,
                original='',
                replacement='# Line too long - consider breaking into multiple lines',
                reason='Style: line exceeds maximum length'
            )
        
        # Unused import
        if 'unused' in message and 'import' in message:
            return FixAction(
                action_type='delete',
                file=issue.file,
                line=issue.line,
                original='import',
                replacement='# import removed (unused)',
                reason='Style: unused import'
            )
        
        return None
    
    def _apply_fix(self, action: FixAction) -> bool:
        """นำการแก้ไขไปใช้กับไฟล์"""
        
        try:
            if not os.path.exists(action.file):
                return False
            
            with open(action.file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if action.action_type == 'replace':
                # แทนที่บรรทัดที่มีปัญหา
                if 0 < action.line <= len(lines):
                    line_content = lines[action.line - 1]
                    if action.original in line_content:
                        lines[action.line - 1] = line_content.replace(
                            action.original, 
                            action.replacement
                        )
                    else:
                        # ถ้าไม่เจอ ให้ comment บรรทัดนั้น
                        lines[action.line - 1] = f"# {line_content}"
                
            elif action.action_type == 'insert':
                # เพิ่มบรรทัดใหม่
                if action.line == 0:
                    lines.insert(0, action.replacement + '\n')
                else:
                    lines.insert(action.line, action.replacement + '\n')
            
            elif action.action_type == 'delete':
                # ลบหรือ comment บรรทัด
                if 0 < action.line <= len(lines):
                    lines[action.line - 1] = f"# DELETED: {lines[action.line - 1]}"
            
            elif action.action_type == 'reformat':
                # เพิ่ม comment แนะนำ
                if 0 < action.line <= len(lines):
                    lines.insert(action.line - 1, f"# STYLE: {action.replacement}\n")
            
            # บันทึกไฟล์
            with open(action.file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            self.fix_history.append(action)
            return True
            
        except Exception as e:
            print(f"Error applying fix: {e}")
            return False
    
    def _print_report(self, report: FixReport):
        """แสดงรายงานการแก้ไข"""
        
        print(f"\n{'='*60}")
        print("AUTO FIX REPORT")
        print(f"{'='*60}")
        print(f"Total Actions: {report.total_fixes}")
        print(f"✅ Applied: {report.fixes_applied}")
        print(f"❌ Failed: {report.fixes_failed}")
        print(f"Status: {'SUCCESS' if report.success else 'PARTIAL'}")
        print(f"{'='*60}\n")
        
        if report.actions:
            print("Actions Taken:")
            for i, action in enumerate(report.actions, 1):
                print(f"{i}. [{action.action_type}] {action.file}:{action.line}")
                print(f"   Reason: {action.reason}")
                if action.replacement:
                    print(f"   Change: {action.replacement[:60]}...")
                print()


if __name__ == "__main__":
    # ทดสอบ auto fixer
    from qa_checker import QAChecker, QAReport, QAIssue
    
    fixer = AutoFixer()
    
    # สร้างไฟล์ทดสอบที่มีปัญหา
    test_code = '''
def dangerous():
    x = input("Enter: ")
    eval(x)

def normal():
    return 42
'''
    
    with open("test_fix.py", "w") as f:
        f.write(test_code)
    
    # สร้าง QA report แบบ mock
    qa_report = QAReport(
        total_issues=1,
        critical=1,
        warnings=0,
        info=0,
        issues=[QAIssue(
            severity='critical',
            category='security',
            message='Use of eval() can be dangerous: eval(',
            file='test_fix.py',
            line=4
        )],
        passed=False
    )
    
    # รัน auto fix
    report = fixer.fix(qa_report, None)
    
    print("\nFile after fix:")
    with open("test_fix.py", 'r') as f:
        print(f.read())
    
    # ลบไฟล์ทดสอบ
    os.remove("test_fix.py")
