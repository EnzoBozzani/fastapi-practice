from sqlmodel import Session, select

from utils.main import verify_password
from database.models import Admin
from database.main import engine


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
