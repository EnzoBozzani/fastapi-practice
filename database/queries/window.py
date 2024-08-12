from sqlmodel import Session, select

from utils.main import check_for_time_collision
from database.models import Window
from database.main import engine
from database import schemas


def get_windows():
    with Session(engine) as db:
        statement = select(Window)
        windows = db.exec(statement).all()
        return windows


def create_window(windowCreate: schemas.WindowCreate):
    window = Window(**windowCreate.model_dump())

    windows = get_windows()

    has_time_collision = check_for_time_collision(
        windows=windows,
        current=window
    )

    print(has_time_collision)

    if (has_time_collision):
        return False

    with Session(engine) as db:
        db.add(window)
        db.commit()
        db.refresh(window)

        return window


def delete_window(id: int):
    with Session(engine) as db:
        statement = select(Window).where(Window.id == id)
        window = db.exec(statement).first()

        if window is None:
            return False

        db.delete(window)
        db.commit()

        return True
