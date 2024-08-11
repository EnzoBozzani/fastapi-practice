from sqlmodel import SQLModel

from main import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    print("Creating tables...")
    create_db_and_tables()
    print("Created tables")


if __name__ == '__main__':
    main()
