from sqlmodel import Session, select

from database import schemas
from database.main import engine
from database.models import Lecture


def get_lectures():
    with Session(engine) as db:
        statement = select(Lecture)
        lectures = db.exec(statement).all()

        return lectures


def create_lecture(lectureCreate: schemas.LectureCreate):
    lecture = Lecture(**lectureCreate.model_dump())

    with Session(engine) as db:
        db.add(lecture)
        db.commit()
        db.refresh(lecture)

        return lecture


def delete_lecture(id: int):
    with Session(engine) as db:
        statement = select(Lecture).where(Lecture.id == id)
        lecture = db.exec(statement).first()

        if lecture is None:
            return False

        db.delete(lecture)
        db.commit()

        return True
