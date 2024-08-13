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


def delete_speaker(id: int):
    with Session(engine) as db:
        statement = select(Speaker).where(Speaker.id == id)
        speaker = db.exec(statement).first()

        if speaker is None:
            return False

        db.delete(speaker)
        db.commit()

        return True


def update_speaker(id: int, speakerUpdate: schemas.SpeakerUpdate):
    with Session(engine) as db:
        statement = select(Speaker).where(Speaker.id == id)
        speaker = db.exec(statement).first()

        if speaker is None:
            return None

        speaker.name = speakerUpdate.name or speaker.name
        speaker.bio = speakerUpdate.bio or speaker.bio
        speaker.company = speakerUpdate.company or speaker.company
        speaker.linkedin = speakerUpdate.linkedin or speaker.linkedin
        speaker.image = speakerUpdate.image or speaker.image

        db.add(speaker)
        db.commit()
        db.refresh(speaker)

        return speaker
