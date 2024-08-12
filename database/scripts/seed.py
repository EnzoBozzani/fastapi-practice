from sqlmodel import Session

from database.models import Window, Speaker, Lecture
from database.main import engine
from utils.constants import BIO_1, BIO_2, BIO_3


def create_windows():
    window_1 = Window(
        id=1,
        title="Abertura",
        start="09:00",
        end="10:00",
        speaker_id=1
    )
    window_2 = Window(
        id=2,
        title="Computação Responsável - sessão somente em inglês",
        start="10:00",
        end="11:15",
        speaker_id=2
    )
    window_3 = Window(
        id=3,
        title="Desenvolvendo tecnologias para uma sociedade responsável",
        start="11:15",
        end="12:15"
    )

    with Session(engine) as db:
        db.add(window_1)
        db.add(window_2)
        db.add(window_3)

        db.commit()


def create_speakers():
    speaker_1 = Speaker(
        id=1,
        name="Bruno Flach",
        company="IBM Research",
        linkedin="https://www.linkedin.com/in/bruno-flach/",
        image="string",
        bio=BIO_2
    )
    speaker_2 = Speaker(
        id=2,
        name="Stacy Hobson",
        company="IBM Research",
        linkedin="https://www.linkedin.com/in/stacy-hobson-4b6105b9/",
        image="string",
        bio=BIO_3
    )
    speaker_3 = Speaker(
        id=3,
        name="Mariana Borges",
        company="F. A. Chateaubriand",
        linkedin="https://www.linkedin.com/in/marianagoesborges/",
        image="string",
        bio=BIO_1
    )

    with Session(engine) as db:
        db.add(speaker_1)
        db.add(speaker_2)
        db.add(speaker_3)

        db.commit()


def create_lectures():
    lecture_1 = Lecture(
        title="IA Responsável - desenvolvendo modelos de linguagem responsáveis e inclusivos",  # noqa: E501
        speaker_id=3,
        window_id=3,
    )
    lecture_2 = Lecture(
        title="Quantum Responsável - desenvolvimento responsável e inclusivo e uso da computação quântica",  # noqa: E501
        speaker_id=3,
        window_id=3,
    )
    lecture_3 = Lecture(
        title="Ciência avançada responsável - o papel da tecnologia emergente e da ciência na sustentabilidade",  # noqa: E501
        speaker_id=3,
        window_id=3,
    )

    with Session(engine) as db:
        db.add(lecture_1)
        db.add(lecture_2)
        db.add(lecture_3)

        db.commit()


def main():
    print("Seeding database...")
    create_speakers()
    create_windows()
    create_lectures()
    print("Seeding ended")


if __name__ == "__main__":
    main()
