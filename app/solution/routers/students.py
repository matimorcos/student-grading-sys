from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from typing import List
from solution.models.models import StudentCreate, StudentResponse, SubjectCreate, SubjectResponse, PracticalWorkCreate, PracticalWorkResponse, GradeRequest, GradeBase, GradeCreate, GradeResponse
from core.schemas import Student, Subject, PracticalWork, Grade
from config.config import get_db, DATABASE_URL 
from solution.services.messages import send_email
import sys 
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'solution')))

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/students/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        db_student = Student(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/students/batch/", response_model=List[StudentResponse])
def create_students(students: List[StudentCreate], db: Session = Depends(get_db)):
    try:
        db_students = []
        for student in students:
            db_student = Student(**student.dict())
            db.add(db_student)
            db.commit()
            db.refresh(db_student)
            db_students.append(db_student)
        return db_students
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")    

@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/subjects/", response_model=SubjectResponse)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    db_subject = Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.get("/subjects/", response_model=List[SubjectResponse])
def get_subject(db: Session = Depends(get_db)):
    return db.query(Subject).all()

@router.post("/practicalworks/", response_model=PracticalWorkResponse)
def create_practical_work(practical_work: PracticalWorkCreate, db: Session = Depends(get_db)):
    try:
        db_practical_work = PracticalWork(**practical_work.dict())
        db.add(db_practical_work)
        db.commit()
        db.refresh(db_practical_work)
        return db_practical_work
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/practicalworks/", response_model=List[PracticalWorkResponse])
def get_practical_works(db: Session = Depends(get_db)):
    return db.query(PracticalWork).all()

@router.get("/practicalwork/{pw_id}/guidelines/")
def get_guidelines_and_achievements(pw_id: str, db: Session = Depends(get_db)):

    practical_work = db.query(PracticalWork).filter(PracticalWork.pw_id == pw_id).first()
    if not practical_work:
        raise HTTPException(status_code=404, detail="Practical work not found")

    guidelines = {
        "guideline_1": {
            "guideline_id": practical_work.guideline_1_id,
            "achievements": [
                {
                    "achievement_id": practical_work.achievement_1_g1_id,
                    "description": practical_work.achievement_1_g1_description,
                    "score": practical_work.achievement_1_g1_score,
                },
                {
                    "achievement_id": practical_work.achievement_2_g1_id,
                    "description": practical_work.achievement_2_g1_description,
                    "score": practical_work.achievement_2_g1_score,
                },
                {
                    "achievement_id": practical_work.achievement_3_g1_id,
                    "description": practical_work.achievement_3_g1_description,
                    "score": practical_work.achievement_3_g1_score,
                }
            ]
        },
        "guideline_2": {
            "guideline_id": practical_work.guideline_2_id,
            "achievements": [
                {
                    "achievement_id": practical_work.achievement_1_g2_id,
                    "description": practical_work.achievement_1_g2_description,
                    "score": practical_work.achievement_1_g2_score,
                },
                {
                    "achievement_id": practical_work.achievement_2_g2_id,
                    "description": practical_work.achievement_2_g2_description,
                    "score": practical_work.achievement_2_g2_score,
                },
                {
                    "achievement_id": practical_work.achievement_3_g2_id,
                    "description": practical_work.achievement_3_g2_description,
                    "score": practical_work.achievement_3_g2_score,
                }
            ]
        },
        "guideline_3": {
            "guideline_id": practical_work.guideline_3_id,
            "achievements": [
                {
                    "achievement_id": practical_work.achievement_1_g3_id,
                    "description": practical_work.achievement_1_g3_description,
                    "score": practical_work.achievement_1_g3_score,
                },
                {
                    "achievement_id": practical_work.achievement_2_g3_id,
                    "description": practical_work.achievement_2_g3_description,
                    "score": practical_work.achievement_2_g3_score,
                },
                {
                    "achievement_id": practical_work.achievement_3_g3_id,
                    "description": practical_work.achievement_3_g3_description,
                    "score": practical_work.achievement_3_g3_score,
                }
            ]
        }
    }

    return {"pw_id": pw_id, "guidelines": guidelines}

@router.post("/gradestudent/", response_model=GradeResponse)
def grade_student(
    request: GradeRequest,
    db: Session = Depends(get_db)
):
    student_id = request.student_id
    pw_id = request.pw_id
    guidelines = request.guidelines

    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    practical_work = db.query(PracticalWork).filter(PracticalWork.pw_id == pw_id).first()
    if not practical_work:
        raise HTTPException(status_code=404, detail="Practical work not found")

    scores = {
        practical_work.achievement_1_g1_id: practical_work.achievement_1_g1_score,
        practical_work.achievement_2_g1_id: practical_work.achievement_2_g1_score,
        practical_work.achievement_3_g1_id: practical_work.achievement_3_g1_score,
        practical_work.achievement_1_g2_id: practical_work.achievement_1_g2_score,
        practical_work.achievement_2_g2_id: practical_work.achievement_2_g2_score,
        practical_work.achievement_3_g2_id: practical_work.achievement_3_g2_score,
        practical_work.achievement_1_g3_id: practical_work.achievement_1_g3_score,
        practical_work.achievement_2_g3_id: practical_work.achievement_2_g3_score,
        practical_work.achievement_3_g3_id: practical_work.achievement_3_g3_score,
    }

    final_score = 0
    achievements_description = []

    for guideline in guidelines:
        for achievement in guideline.achievements:
            if achievement.achievement_id not in scores:
                raise HTTPException(status_code=400, detail=f"Achievement ID {achievement.achievement_id} not found")
            
            final_score += scores[achievement.achievement_id]
            achievements_description.append(achievement.description)

    new_grade = Grade(
        student_id=student_id,
        pw_id=pw_id,
        score=final_score,
        achievements_description=" | ".join(achievements_description)
    )

    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)

    return GradeResponse(
        student_id=new_grade.student_id,
        pw_id=new_grade.pw_id,
        score=new_grade.score,
        achievements_description=new_grade.achievements_description
    )

@router.post("/submitgrade/", response_model=GradeResponse)
def submit_grade(
    request: GradeRequest,
    db: Session = Depends(get_db)
):
    student_id = request.student_id
    pw_id = request.pw_id
    guidelines = request.guidelines

    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    practical_work = db.query(PracticalWork).filter(PracticalWork.pw_id == pw_id).first()
    if not practical_work:
        raise HTTPException(status_code=404, detail="Practical work not found")

    scores = {
        practical_work.achievement_1_g1_id: practical_work.achievement_1_g1_score,
        practical_work.achievement_2_g1_id: practical_work.achievement_2_g1_score,
        practical_work.achievement_3_g1_id: practical_work.achievement_3_g1_score,
        practical_work.achievement_1_g2_id: practical_work.achievement_1_g2_score,
        practical_work.achievement_2_g2_id: practical_work.achievement_2_g2_score,
        practical_work.achievement_3_g2_id: practical_work.achievement_3_g2_score,
        practical_work.achievement_1_g3_id: practical_work.achievement_1_g3_score,
        practical_work.achievement_2_g3_id: practical_work.achievement_2_g3_score,
        practical_work.achievement_3_g3_id: practical_work.achievement_3_g3_score,
    }

    final_score = 0
    achievements_description = []

    for guideline in guidelines:
        for achievement in guideline.achievements:
            if achievement.achievement_id not in scores:
                raise HTTPException(status_code=400, detail=f"Achievement ID {achievement.achievement_id} not found")
            
            final_score += scores[achievement.achievement_id]
            achievements_description.append(achievement.description)

    new_grade = Grade(
        student_id=student_id,
        pw_id=pw_id,
        score=final_score,
        achievements_description=" | ".join(achievements_description)
    )

    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)

    subject = "Your Practical Work Grade"
    to_email = student.student_username
    message = (
        f"Hello {student.student_names},\n\n"
        f"Your score for the Guideline {guidelines} from the Practical Work {pw_id} is: {final_score}/100.\n"
        f"Observations:\n- " + "\n- ".join(achievements_description) + "\n\n"
        "You can fix the observations and resubmit the grade.\nBest regards."
    )
    
    try:
        send_email(subject=subject, to_email=student.student_username, email_body=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

    return GradeResponse(
        grade_id=str(new_grade.grade_id),
        student_id=str(new_grade.student_id),
        pw_id=new_grade.pw_id,
        score=new_grade.score,
        achievements_description=new_grade.achievements_description
    )
