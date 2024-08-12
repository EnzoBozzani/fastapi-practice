from sqlmodel import SQLModel, Session

from .models import Admin
from .main import engine

from utils.main import get_password_hash


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def create_user():
    user = Admin(
        email="enzo@ibm.com", hashed_password=get_password_hash("123456")
    )

    with Session(engine) as db:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user


def main():
    print("Creating tables...")
    create_db_and_tables()
    create_user()
    print("Created tables")


if __name__ == '__main__':
    main()
