from sqlmodel import Session

from .models import Window
from .main import engine


def create_windows():
    window_1 = Window(title="First Window", start="09:00", end="10:00")
    window_2 = Window(title="Second window", start="10:00", end="11:00")

    with Session(engine) as db:
        db.add(window_1)
        db.add(window_2)

        db.commit()


def main():
    print("Seeding database...")
    create_windows()
    print("Seeding ended")


if __name__ == "__main__":
    main()
