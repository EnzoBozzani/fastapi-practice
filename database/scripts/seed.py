from sqlmodel import Session

from database.models import Window, Speaker
from database.main import engine
from utils.constants import BIO_1, BIO_2, BIO_3


def create_windows():
    window_1 = Window(title="First Window", start="09:00", end="10:00")
    window_2 = Window(title="Second window", start="10:00", end="11:00")
    window_3 = Window(title="Third window", start="11:00", end="12:00")

    with Session(engine) as db:
        db.add(window_1)
        db.add(window_2)
        db.add(window_3)

        db.commit()


def create_speakers():
    speaker_1 = Speaker(
        name="Mariana Borges",
        company="F. A. Chateaubriand",
        linkedin="https://www.linkedin.com/in/marianagoesborges/",
        image="string",
        bio=BIO_1
    )
    speaker_2 = Speaker(
        name="Bruno Flach",
        company="IBM Research",
        linkedin="https://www.linkedin.com/in/bruno-flach/",
        image="string",
        bio=BIO_2
    )
    speaker_3 = Speaker(
        name="Stacy Hobson",
        company="IBM Research",
        linkedin="https://www.linkedin.com/in/stacy-hobson-4b6105b9/",
        image="string",
        bio=BIO_3
    )

    with Session(engine) as db:
        db.add(speaker_1)
        db.add(speaker_2)
        db.add(speaker_3)

        db.commit()


def main():
    print("Seeding database...")
    create_windows()
    create_speakers()
    print("Seeding ended")


if __name__ == "__main__":
    main()
