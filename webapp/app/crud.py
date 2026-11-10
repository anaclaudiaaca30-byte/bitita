from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import Student
from .schemas import StudentCreate, StudentUpdate


def get_students(db: Session):
    return db.query(Student).order_by(Student.id.asc()).all()


def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student: StudentUpdate):
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        return None

    for key, value in student.model_dump().items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_student(db: Session, student_id: int):
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True



def get_dashboard(db: Session):
    nacionalidade = func.lower(func.trim(Student.nationality))

    dados = (
        db.query(nacionalidade, func.count(Student.id))
        .group_by(nacionalidade)
        .order_by(func.count(Student.id).desc())
        .all()
    )

    return [
        {
            "label": label.title() if label else "Não informada",
            "value": value
        }
        for label, value in dados
    ]

