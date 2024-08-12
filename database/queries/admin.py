from sqlmodel import Session, select

from utils.main import verify_password, get_password_hash
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


def add_admin(email: str, password: str):
    existing_admin = get_admin(email)

    if existing_admin is not None:
        return None

    hashed_password = get_password_hash(password)

    admin = Admin(
        email=email,
        hashed_password=hashed_password
    )

    with Session(engine) as db:
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin
