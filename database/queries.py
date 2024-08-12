from sqlmodel import Session, select

from utils.main import verify_password
from utils.main import check_for_time_collision

from .models import Window, Admin
from .main import engine
from . import schemas


def authenticate_admin(email: str, password: str):
    with Session(engine) as db:
        statement = select(Admin).where(Admin.email == email)
        admin = db.exec(statement).first()

        if not admin:
            return False

        if not verify_password(password, admin.hashed_password):
            return False

        return admin


def get_admin(email: str):
    with Session(engine) as db:
        statement = select(Admin).where(Admin.email == email)
        admin = db.exec(statement).first()

        return admin


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
