#!/usr/bin/env python3
"""
Auto Dev Agent - ระบบพัฒนาซอฟต์แวร์อัตโนมัติ

Main entry point ที่รวมทุก components เข้าด้วยกัน
"""
import sys
import os
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Import modules
from analyzer import RequirementAnalyzer, AnalysisResult
from workflow_generator import WorkflowGenerator, Workflow
from code_generator import CodeGenerator, CodeGenerationResult
from test_runner import TestRunner, TestReport
from qa_checker import QAChecker, QAReport
from auto_fixer import AutoFixer, FixReport

console = Console()

class AutoDevAgent:
    """Main agent class ที่ประสานงานทุก components"""
    
    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
        self.analyzer = RequirementAnalyzer()
        self.workflow_generator = WorkflowGenerator()
        self.code_generator = CodeGenerator()
        self.test_runner = TestRunner()
        self.qa_checker = QAChecker()
        self.auto_fixer = AutoFixer()
        
        # เก็บผลลัพธ์แต่ละขั้นตอน
        self.analysis_result: AnalysisResult = None
        self.workflow: Workflow = None
        self.code_result: CodeGenerationResult = None
        self.test_report: TestReport = None
        self.qa_report: QAReport = None
        self.fix_report: FixReport = None
    
    def run(self, user_request: str, output_dir: str = "output", auto_fix: bool = True) -> bool:
        """รันกระบวนการพัฒนาทั้งหมด"""
        
        console.print(Panel.fit(
            f"[bold blue]🤖 Auto Dev Agent[/bold blue]\n"
            f"Processing: {user_request[:50]}{'...' if len(user_request) > 50 else ''}",
            border_style="blue"
        ))
        
        # สร้าง output directory
        os.makedirs(output_dir, exist_ok=True)
        os.chdir(output_dir)
        
        try:
            # Step 1: Analyze Requirements
            console.print("\n[bold green]Step 1/6:[/bold green] Analyzing Requirements...")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task("Analyzing...", total=None)
                self.analysis_result = self.analyzer.analyze(user_request)
            
            self._print_analysis_summary()
            
            # Step 2: Generate Workflow
            console.print("\n[bold green]Step 2/6:[/bold green] Generating Workflow...")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task("Generating workflow...", total=None)
                self.workflow = self.workflow_generator.generate(self.analysis_result)
            
            self._print_workflow_summary()
            
            # Step 3: Generate Code
            console.print("\n[bold green]Step 3/6:[/bold green] Generating Code...")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task("Writing code files...", total=None)
                self.code_result = self.code_generator.generate(self.workflow, self.analysis_result)
                self.code_generator.save_files(self.code_result, ".")
            
            console.print(f"[green]✓ Generated {len(self.code_result.files)} files[/green]")
            
            # Step 4: Run Tests
            console.print("\n[bold green]Step 4/6:[/bold green] Running Tests...")
            if os.path.exists("test_main.py"):
                self.test_report = self.test_runner.run_tests("test_main.py")
            else:
                console.print("[yellow]⚠ No test file found, skipping tests[/yellow]")
                self.test_report = TestReport(
                    total_tests=0, passed=0, failed=0, results=[], success_rate=0.0
                )
            
            # Step 5: QA Check
            console.print("\n[bold green]Step 5/6:[/bold green] Running QA Check...")
            py_files = [f for f in os.listdir('.') if f.endswith('.py') and 
                       f not in ['qa_checker.py', 'auto_fixer.py']]
            self.qa_report = self.qa_checker.check(py_files)
            
            # Step 6: Auto Fix (if needed and enabled)
            if auto_fix and (not self.qa_report.passed or (self.test_report and self.test_report.failed > 0)):
                console.print("\n[bold green]Step 6/6:[/bold green] Attempting Auto Fixes...")
                self.fix_report = self.auto_fixer.fix(self.qa_report, self.test_report)
                
                # Re-run tests and QA after fixes
                if self.fix_report and self.fix_report.fixes_applied > 0:
                    console.print("\n[bold yellow]Re-validating after fixes...[/bold yellow]")
                    self.test_report = self.test_runner.run_tests("test_main.py")
                    self.qa_report = self.qa_checker.check(py_files)
            else:
                if self.qa_report.passed and (not self.test_report or self.test_report.failed == 0):
                    console.print("\n[green]✓ All checks passed, no fixes needed![/green]")
                else:
                    console.print("\n[yellow]⚠ Auto-fix disabled or no critical issues to fix[/yellow]")
            
            # Final Summary
            self._print_final_summary()
            
            # Return success status
            return (self.qa_report.passed and 
                   (not self.test_report or self.test_report.failed == 0))
            
        except Exception as e:
            console.print(f"\n[bold red]❌ Error: {str(e)}[/bold red]")
            import traceback
            traceback.print_exc()
            return False
    
    def _print_analysis_summary(self):
        """แสดงสรุปการวิเคราะห์"""
        table = Table(title="Analysis Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Requirements Found", str(len(self.analysis_result.requirements)))
        table.add_row("Complexity", self.analysis_result.estimated_complexity)
        table.add_row("Technologies", ", ".join(self.analysis_result.suggested_technologies[:3]))
        
        console.print(table)
        
        console.print("\n[bold]Top Requirements:[/bold]")
        for i, req in enumerate(self.analysis_result.requirements[:5], 1):
            priority_color = {"high": "red", "medium": "yellow", "low": "green"}[req.priority]
            console.print(f"  {i}. [{priority_color}]{req.priority.upper()}[/{priority_color}] {req.description}")
    
    def _print_workflow_summary(self):
        """แสดงสรุป workflow"""
        table = Table(title="Workflow Summary")
        table.add_column("Task", style="cyan")
        table.add_column("Time (min)", style="green")
        
        for task in self.workflow.tasks:
            table.add_row(task.name, str(task.estimated_time))
        
        table.add_row("[bold]Total[/bold]", f"[bold]{self.workflow.total_estimated_time}[/bold]")
        console.print(table)
    
    def _print_final_summary(self):
        """แสดงสรุปสุดท้าย"""
        console.print("\n" + "="*60)
        console.print("[bold blue]FINAL SUMMARY[/bold blue]")
        console.print("="*60)
        
        # Test Results
        if self.test_report and self.test_report.total_tests > 0:
            test_status = "✅ PASSED" if self.test_report.failed == 0 else "❌ FAILED"
            console.print(f"\n[bold]Tests:[/bold] {test_status}")
            console.print(f"  Passed: {self.test_report.passed}/{self.test_report.total_tests}")
            console.print(f"  Success Rate: {self.test_report.success_rate:.1f}%")
        
        # QA Results
        qa_status = "✅ PASSED" if self.qa_report.passed else "❌ NEEDS ATTENTION"
        console.print(f"\n[bold]QA Check:[/bold] {qa_status}")
        console.print(f"  Critical Issues: {self.qa_report.critical}")
        console.print(f"  Warnings: {self.qa_report.warnings}")
        console.print(f"  Info: {self.qa_report.info}")
        
        # Auto Fix Results
        if self.fix_report:
            fix_status = "✅ SUCCESS" if self.fix_report.success else "⚠ PARTIAL"
            console.print(f"\n[bold]Auto Fix:[/bold] {fix_status}")
            console.print(f"  Applied: {self.fix_report.fixes_applied}")
            console.print(f"  Failed: {self.fix_report.fixes_failed}")
        
        # Overall Status
        overall_success = (self.qa_report.passed and 
                          (not self.test_report or self.test_report.failed == 0))
        
        console.print("\n" + "="*60)
        if overall_success:
            console.print("[bold green]🎉 PROJECT COMPLETED SUCCESSFULLY![/bold green]")
        else:
            console.print("[bold yellow]⚠ PROJECT COMPLETED WITH ISSUES - Manual Review Recommended[/bold yellow]")
        console.print("="*60)
        
        console.print(f"\n[bold]Output Directory:[/bold] {os.getcwd()}")
        console.print("[bold]Files Created:[/bold]")
        for file in self.code_result.files if self.code_result else []:
            console.print(f"  • {file.filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Auto Dev Agent - Automated Software Development System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "สร้างโปรแกรมคำนวณภาษี"
  python main.py "Create a todo list app with database" --output my_todo
  python main.py "Build a weather API client" --no-auto-fix
        """
    )
    
    parser.add_argument(
        "request",
        type=str,
        help="คำอธิบายโปรเจคที่ต้องการ (ภาษาไทยหรืออังกฤษ)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output",
        help="Directory สำหรับเก็บผลลัพธ์ (default: output)"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="default",
        help="ชื่อโมเดล AI ที่จะใช้ (default: default)"
    )
    
    parser.add_argument(
        "--no-auto-fix",
        action="store_true",
        help="ปิดการใช้งาน auto-fix"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="แสดงรายละเอียดเพิ่มเติม"
    )
    
    args = parser.parse_args()
    
    # Create and run agent
    agent = AutoDevAgent(model_name=args.model)
    success = agent.run(
        user_request=args.request,
        output_dir=args.output,
        auto_fix=not args.no_auto_fix
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
