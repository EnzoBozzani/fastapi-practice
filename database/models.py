from sqlmodel import Field, SQLModel, Relationship


class Admin(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    hashed_password: str


class Window(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    start: str
    end: str

    lectures: list["Lecture"] = Relationship(
        back_populates="window", cascade_delete=True
    )


class Speaker(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    company: str
    linkedin: str
    image: str
    bio: str

    lectures: list["Lecture"] = Relationship(
        back_populates="speaker", cascade_delete=True
    )


class Lecture(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    speaker_id: int | None = Field(
        default=None, foreign_key="speaker.id", nullable=False,
        ondelete="CASCADE"
    )
    window_id: int | None = Field(
        default=None, foreign_key="window.id", nullable=False,
        ondelete="CASCADE"
    )

    speaker: Speaker | None = Relationship(back_populates="lectures")
    window: Window | None = Relationship(back_populates="lectures")
