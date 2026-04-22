"""
Analyzer Module - วิเคราะห์ความต้องการและแยกย่อยเป็นงานเล็กๆ
"""
from typing import List, Dict, Any
from pydantic import BaseModel
import re

class Requirement(BaseModel):
    id: str
    description: str
    priority: str  # high, medium, low
    category: str  # feature, bugfix, enhancement, test
    dependencies: List[str] = []

class AnalysisResult(BaseModel):
    original_request: str
    requirements: List[Requirement]
    estimated_complexity: str  # low, medium, high
    suggested_technologies: List[str]

class RequirementAnalyzer:
    def __init__(self, model_client=None):
        self.model_client = model_client
    
    def analyze(self, user_request: str) -> AnalysisResult:
        """วิเคราะห์ความต้องการจากคำขอของผู้ใช้"""
        
        # แยกย่อยความต้องการด้วย regex และ rules-based approach
        requirements = self._extract_requirements(user_request)
        
        # วิเคราะห์ความซับซ้อน
        complexity = self._estimate_complexity(requirements)
        
        # เสนอเทคโนโลยีที่เหมาะสม
        technologies = self._suggest_technologies(user_request, requirements)
        
        return AnalysisResult(
            original_request=user_request,
            requirements=requirements,
            estimated_complexity=complexity,
            suggested_technologies=technologies
        )
    
    def _extract_requirements(self, text: str) -> List[Requirement]:
        """แยกความต้องการออกเป็นข้อๆ"""
        requirements = []
        
        # แยกประโยคด้วยเครื่องหมายต่างๆ
        sentences = re.split(r'[\.!?।]', text)
        
        priority_keywords = {
            'high': ['ต้อง', 'จำเป็น', 'สำคัญ', 'หลัก', 'core', 'must'],
            'medium': ['ควร', 'เหมาะสม', 'รอง', 'secondary', 'should'],
            'low': ['อาจ', 'ถ้ามีเวลา', 'เสริม', 'optional', 'nice to have']
        }
        
        category_keywords = {
            'feature': ['ฟีเจอร์', 'ฟังก์ชัน', 'ความสามารถ', 'feature', 'function'],
            'test': ['ทดสอบ', 'เทส', 'ตรวจสอบ', 'test', 'verify'],
            'enhancement': ['ปรับปรุง', 'พัฒนา', 'optimize', 'improve'],
            'bugfix': ['แก้ไข', 'ซ่อม', 'แก้บั๊ก', 'fix', 'bug']
        }
        
        req_id = 1
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 5:
                continue
            
            # กำหนด priority
            priority = 'medium'
            sentence_lower = sentence.lower()
            for p, keywords in priority_keywords.items():
                if any(kw in sentence_lower for kw in keywords):
                    priority = p
                    break
            
            # กำหนด category
            category = 'feature'
            for c, keywords in category_keywords.items():
                if any(kw in sentence_lower for kw in keywords):
                    category = c
                    break
            
            requirements.append(Requirement(
                id=f"REQ-{req_id:03d}",
                description=sentence,
                priority=priority,
                category=category
            ))
            req_id += 1
        
        # จัดเรียงตาม priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        requirements.sort(key=lambda x: priority_order[x.priority])
        
        return requirements
    
    def _estimate_complexity(self, requirements: List[Requirement]) -> str:
        """ประเมินความซับซ้อนของโปรเจค"""
        if len(requirements) <= 3:
            return 'low'
        elif len(requirements) <= 7:
            return 'medium'
        else:
            return 'high'
    
    def _suggest_technologies(self, request: str, requirements: List[Requirement]) -> List[str]:
        """เสนอเทคโนโลยีที่เหมาะสม"""
        technologies = []
        request_lower = request.lower()
        
        # ตรวจสอบประเภทของแอปพลิเคชัน
        if any(kw in request_lower for kw in ['web', 'website', 'เว็บ']):
            technologies.extend(['HTML/CSS', 'JavaScript', 'React/Vue'])
        
        if any(kw in request_lower for kw in ['api', 'backend', 'server']):
            technologies.extend(['Python/FastAPI', 'Node.js/Express'])
        
        if any(kw in request_lower for kw in ['database', 'ฐานข้อมูล', 'db']):
            technologies.extend(['PostgreSQL', 'SQLite'])
        
        if any(kw in request_lower for kw in ['ui', 'interface', 'gui', 'desktop']):
            technologies.extend(['Tkinter', 'PyQt', 'Electron'])
        
        if any(kw in request_lower for kw in ['test', 'testing', 'automated']):
            technologies.extend(['pytest', 'unittest'])
        
        # เพิ่ม default technologies ถ้าไม่มี
        if not technologies:
            technologies = ['Python', 'SQLite']
        
        return list(set(technologies))  # ลบซ้ำ


if __name__ == "__main__":
    # ทดสอบ analyzer
    analyzer = RequirementAnalyzer()
    
    test_request = """
    ฉันต้องการสร้างโปรแกรมคำนวณภาษีเงินได้ 
    ต้องมีฟีเจอร์กรอกข้อมูลรายได้และค่าใช้จ่าย
    ควรคำนวณภาษีอัตโนมัติตามขั้นบันได
    ต้องแสดงผลลัพธ์เป็นตาราง
    อาจจะมีกราฟแสดงสัดส่วนด้วยถ้ามีเวลา
    """
    
    result = analyzer.analyze(test_request)
    
    print(f"Original Request: {result.original_request}")
    print(f"\nComplexity: {result.estimated_complexity}")
    print(f"Suggested Technologies: {', '.join(result.suggested_technologies)}")
    print("\nRequirements:")
    for req in result.requirements:
        print(f"  [{req.id}] ({req.priority}) {req.description}")
