from sqlmodel import Session, select

from .models import Window, Admin
from .main import engine
from utils.main import verify_password

from . import schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(
#       email=user.email, hashed_password=fake_hashed_password
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


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

    with Session(engine) as db:
        db.add(window)
        db.commit()
        db.refresh(window)

        return window
