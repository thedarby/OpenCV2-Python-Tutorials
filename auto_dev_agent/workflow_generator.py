"""
Workflow Generator - สร้าง workflow ย่อยๆ จากความต้องการ
"""
from typing import List, Dict, Any
from pydantic import BaseModel
from analyzer import Requirement, AnalysisResult

class WorkflowTask(BaseModel):
    id: str
    name: str
    description: str
    requirement_ids: List[str]  # เชื่อมโยงกับ requirements
    estimated_time: int  # นาที
    status: str = 'pending'  # pending, in_progress, completed, failed
    dependencies: List[str] = []  # task ids ที่ต้องทำก่อน

class Workflow(BaseModel):
    project_name: str
    tasks: List[WorkflowTask]
    total_estimated_time: int

class WorkflowGenerator:
    def __init__(self):
        pass
    
    def generate(self, analysis_result: AnalysisResult) -> Workflow:
        """สร้าง workflow จากผลการวิเคราะห์"""
        
        tasks = []
        task_id = 1
        
        # Group requirements by category
        req_by_category = {}
        for req in analysis_result.requirements:
            if req.category not in req_by_category:
                req_by_category[req.category] = []
            req_by_category[req.category].append(req)
        
        # สร้าง task สำหรับแต่ละ category
        # 1. Setup & Planning
        if analysis_result.requirements:
            tasks.append(WorkflowTask(
                id=f"TASK-{task_id:03d}",
                name="Project Setup",
                description="ตั้งค่าโปรเจคและเตรียม environment",
                requirement_ids=[],
                estimated_time=15
            ))
            task_id += 1
        
        # 2. Core Features
        if 'feature' in req_by_category:
            feature_reqs = req_by_category['feature']
            for i, req in enumerate(feature_reqs, 1):
                tasks.append(WorkflowTask(
                    id=f"TASK-{task_id:03d}",
                    name=f"Implement Feature {i}",
                    description=req.description,
                    requirement_ids=[req.id],
                    estimated_time=30,
                    dependencies=[f"TASK-{task_id-1:03d}"] if task_id > 1 else []
                ))
                task_id += 1
        
        # 3. Testing
        if 'feature' in req_by_category or len(analysis_result.requirements) > 0:
            all_feature_req_ids = [req.id for req in analysis_result.requirements 
                                   if req.category == 'feature']
            
            tasks.append(WorkflowTask(
                id=f"TASK-{task_id:03d}",
                name="Write Tests",
                description="เขียนและรันการทดสอบ",
                requirement_ids=all_feature_req_ids,
                estimated_time=20,
                dependencies=[t.id for t in tasks[-2:]] if len(tasks) >= 2 else []
            ))
            task_id += 1
        
        # 4. QA & Code Review
        tasks.append(WorkflowTask(
            id=f"TASK-{task_id:03d}",
            name="QA Check",
            description="ตรวจสอบคุณภาพโค้ดและรัน linters",
            requirement_ids=[req.id for req in analysis_result.requirements],
            estimated_time=15,
            dependencies=[f"TASK-{task_id-1:03d}"] if task_id > 1 else []
        ))
        task_id += 1
        
        # 5. Documentation
        tasks.append(WorkflowTask(
            id=f"TASK-{task_id:03d}",
            name="Documentation",
            description="เขียนเอกสารและ README",
            requirement_ids=[],
            estimated_time=10,
            dependencies=[]
        ))
        task_id += 1
        
        # คำนวณเวลาทั้งหมด
        total_time = sum(task.estimated_time for task in tasks)
        
        return Workflow(
            project_name=f"Auto Generated Project",
            tasks=tasks,
            total_estimated_time=total_time
        )
    
    def print_workflow(self, workflow: Workflow):
        """แสดง workflow แบบ readable"""
        print(f"\n{'='*60}")
        print(f"PROJECT: {workflow.project_name}")
        print(f"Total Estimated Time: {workflow.total_estimated_time} minutes")
        print(f"{'='*60}\n")
        
        for i, task in enumerate(workflow.tasks, 1):
            deps = f" (depends on: {', '.join(task.dependencies)})" if task.dependencies else ""
            reqs = f" [{', '.join(task.requirement_ids)}]" if task.requirement_ids else ""
            
            print(f"{i}. {task.name}{reqs}{deps}")
            print(f"   Description: {task.description}")
            print(f"   Estimated Time: {task.estimated_time} min")
            print(f"   Status: {task.status}")
            print()


if __name__ == "__main__":
    # ทดสอบ workflow generator
    from analyzer import RequirementAnalyzer, Requirement
    
    analyzer = RequirementAnalyzer()
    test_request = """
    ฉันต้องการสร้างโปรแกรมคำนวณภาษีเงินได้
    ต้องมีฟีเจอร์กรอกข้อมูลรายได้และค่าใช้จ่าย
    ควรคำนวณภาษีอัตโนมัติตามขั้นบันได
    ต้องแสดงผลลัพธ์เป็นตาราง
    """
    
    analysis_result = analyzer.analyze(test_request)
    
    generator = WorkflowGenerator()
    workflow = generator.generate(analysis_result)
    
    generator.print_workflow(workflow)
