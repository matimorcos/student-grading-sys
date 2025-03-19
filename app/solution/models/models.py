from pydantic import BaseModel
from typing import List, Optional

class StudentBase(BaseModel):
    student_names: str
    student_username: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    student_id: Optional[int]

    class Config:
        orm_mode = True

class SubjectCreate(BaseModel):
    subject_id: Optional[str]
    subject: str
    subject_description: str
    period_id: str
    year: int
    teaching: str
    teachers_email: str

    class Config:
        orm_mode = True

class SubjectResponse(BaseModel):
    subject_id: Optional[str]
    subject: str
    subject_description: str
    period_id: str
    year: int
    teaching: str
    teachers_email: str

    class Config:
        orm_mode = True
        
class Achievement(BaseModel):
    achievement_id: Optional[str]
    description: str
    score: int

class Guideline(BaseModel):
    guideline_id: Optional[str]
    achievements: List[Achievement]

class PracticalWorkCreate(BaseModel):
    pw_id: Optional[str]
    guideline_1_id: str
    achievement_1_g1_id: str
    achievement_1_g1_description: str
    achievement_1_g1_score: int
    achievement_2_g1_id: str
    achievement_2_g1_description: str
    achievement_2_g1_score: int
    achievement_3_g1_id: str
    achievement_3_g1_description: str
    achievement_3_g1_score: int
    guideline_2_id: str
    achievement_1_g2_id: str
    achievement_1_g2_description: str
    achievement_1_g2_score: int
    achievement_2_g2_id: str
    achievement_2_g2_description: str
    achievement_2_g2_score: int
    achievement_3_g2_id: str
    achievement_3_g2_description: str
    achievement_3_g2_score: int
    guideline_3_id: str
    achievement_1_g3_id: str
    achievement_1_g3_description: str
    achievement_1_g3_score: int
    achievement_2_g3_id: str
    achievement_2_g3_description: str
    achievement_2_g3_score: int
    achievement_3_g3_id: str
    achievement_3_g3_description: str
    achievement_3_g3_score: int
    subject_id: Optional[str]

    class Config:
        orm_mode = True

class PracticalWorkResponse(BaseModel):
    pw_id: Optional[str]
    guideline_1_id: str
    achievement_1_g1_id: str
    achievement_1_g1_description: str
    achievement_1_g1_score: int
    achievement_2_g1_id: str
    achievement_2_g1_description: str
    achievement_2_g1_score: int
    achievement_3_g1_id: str
    achievement_3_g1_description: str
    achievement_3_g1_score: int
    guideline_2_id: str
    achievement_1_g2_id: str
    achievement_1_g2_description: str
    achievement_1_g2_score: int
    achievement_2_g2_id: str
    achievement_2_g2_description: str
    achievement_2_g2_score: int
    achievement_3_g2_id: str
    achievement_3_g2_description: str
    achievement_3_g2_score: int
    guideline_3_id: str
    achievement_1_g3_id: str
    achievement_1_g3_description: str
    achievement_1_g3_score: int
    achievement_2_g3_id: str
    achievement_2_g3_description: str
    achievement_2_g3_score: int
    achievement_3_g3_id: str
    achievement_3_g3_description: str
    achievement_3_g3_score: int
    subject_id: Optional[str]

    class Config:
        orm_mode = True

class GradeBase(BaseModel):
    grade_id: int
    student_id: str
    pw_id: str
    achievements_description: str 
    score: int
    
    class Config:
        orm_mode = True

class GradeCreate(GradeBase):
    pass

class GradeUpdate(GradeBase):
    pass

class GradeResponse(GradeBase):
    grade_id: int
        
class GradeRequest(BaseModel):
    student_id: int
    pw_id: str
    guidelines: List[Guideline]  

    class Config:
        orm_mode = True