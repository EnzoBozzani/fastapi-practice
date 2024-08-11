from pydantic import BaseModel, EmailStr
from sqlmodel import Field


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
    speakerId: str
    windowId: str


class Lecture(LectureBase):
    id: str
    speakerId: str
    windowId: str

    class Config:
        from_attributes = True


class WindowBase(BaseModel):
    title: str = Field(min_length=3, max_length=250)
    start: str = Field(min_length=5, max_length=5)
    end: str = Field(min_length=5, max_length=5)


class WindowCreate(WindowBase):
    pass


class Window(WindowBase):
    id: int
    lectures: list[Lecture] = []

    class Config:
        from_attributes = True


class SpeakerBase(BaseModel):
    name: str
    company: str
    linkedin: str
    image: str
    bio: str


class SpeakerCreate(SpeakerBase):
    pass


class Speaker(SpeakerBase):
    id: int
    lectures: list[Lecture] = []

    class Config:
        from_attributes = True
