from sqlmodel import Session, select

from database import schemas
from utils.main import check_for_time_collision
from database.models import Window
from database.main import engine
from database.queries.speaker import get_speaker


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


def update_window(id: int, windowUpdate: schemas.WindowUpdate):
    with Session(engine) as db:
        statement = select(Window).where(Window.id == id)
        window = db.exec(statement).first()

        if window is None:
            return {
                    'error': 'Window not found!',
                    'status_code': 404
                }

        if windowUpdate.speaker_id is not None:
            speaker = get_speaker(windowUpdate.speaker_id)

            if speaker is None:
                return {
                    'error': 'Speaker no found!',
                    'status_code': 404
                }

        window.title = windowUpdate.title or window.title
        window.start = windowUpdate.start or window.start
        window.end = windowUpdate.end or window.end
        window.speaker_id = windowUpdate.speaker_id or window.speaker_id

        if windowUpdate.start is not None or windowUpdate.end is not None:
            windows = get_windows()

            windows_excluding_current: list[Window] = []

            for w in windows:
                if (w.id != window.id):
                    windows_excluding_current.append(w)

            has_time_collision = check_for_time_collision(
                windows_excluding_current,
                window
            )

            if (has_time_collision):
                return {
                        'error': 'Time collision detected!',
                        'status_code': 400
                    }

        db.add(window)
        db.commit()
        db.refresh(window)

        return {'window': window}
