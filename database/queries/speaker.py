from sqlmodel import Session, select

from database import schemas
from database.main import engine
from database.models import Speaker


def get_speakers():
    with Session(engine) as db:
        statement = select(Speaker)
        speakers = db.exec(statement).all()

        return speakers


def create_speaker(speakerCreate: schemas.SpeakerCreate):
    speaker = Speaker(**speakerCreate.model_dump())

    with Session(engine) as db:
        db.add(speaker)
        db.commit()
        db.refresh(speaker)

        return speaker
