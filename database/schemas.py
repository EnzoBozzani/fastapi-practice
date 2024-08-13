from pydantic import BaseModel, EmailStr, Field
from database.models import Lecture as DbLecture


class AdminBase(BaseModel):
    email: EmailStr = Field(min_length=3, max_length=50)


class AdminCreate(AdminBase):
    password: str = Field(min_length=6, max_length=50)


class Admin(AdminBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True


class LectureBase(BaseModel):
    title: str = Field(min_length=3, max_length=250)


class LectureCreate(LectureBase):
    speaker_id: int
    window_id: int


class Lecture(LectureBase):
    id: int
    speaker_id: int
    window_id: int

    class Config:
        from_attributes = True


class LectureResponse(LectureBase):
    id: int
    speaker_id: int
    window_id: int


class WindowBase(BaseModel):
    title: str = Field(min_length=3, max_length=250)
    start: str = Field(
        min_length=5, max_length=5, pattern="^([01]\d|2[0-3]):[0-5]\d$"  # noqa: W605, E501
    )
    end: str = Field(
        min_length=5, max_length=5, pattern="^([01]\d|2[0-3]):[0-5]\d$"  # noqa: W605, E501
    )


class WindowResponse(WindowBase):
    id: int
    speaker_id: int | None


class WindowCreate(WindowBase):
    speaker_id: int | None
    pass


class Window(WindowBase):
    id: int
    lectures: list[Lecture] = []

    class Config:
        from_attributes = True


class WindowUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=250)
    start: str | None = Field(
        default=None,
        min_length=5,
        max_length=5,
        pattern="^([01]\d|2[0-3]):[0-5]\d$"  # noqa: W605, E501
    )
    end: str | None = Field(
        default=None,
        min_length=5,
        max_length=5,
        pattern="^([01]\d|2[0-3]):[0-5]\d$"  # noqa: W605, E501
    )
    speaker_id: int | None = Field(default=None)


class SpeakerBase(BaseModel):
    name: str
    company: str
    linkedin: str
    image: str
    bio: str


class SpeakerCreate(BaseModel):
    name: str
    company: str
    linkedin: str
    bio: str


class SpeakerResponse(SpeakerBase):
    id: int


class Speaker(SpeakerBase):
    id: int
    lectures: list[Lecture] = []

    class Config:
        from_attributes = True


class SpeakerUpdate(BaseModel):
    name: str | None = Field(default=None)
    company: str | None = Field(default=None)
    linkedin: str | None = Field(default=None)
    image: str | None = Field(default=None)
    bio: str | None = Field(default=None)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class WindowWithLectures(WindowBase):
    id: int
    lectures: list[DbLecture] = []
