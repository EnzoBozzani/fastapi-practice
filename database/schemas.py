from pydantic import BaseModel


class AdminBase(BaseModel):
    email: str


class AdminCreate(AdminBase):
    password: str


class Admin(AdminBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


class LectureBase(BaseModel):
    title: str


class LectureCreate(LectureBase):
    speakerId: str
    windowId: str


class Lecture(LectureBase):
    id: str
    speakerId: str
    windowId: str

    class Config:
        orm_mode = True


class WindowBase(BaseModel):
    title: str
    start: str
    end: str


class WindowCreate(WindowBase):
    pass


class Window(WindowBase):
    id: int
    lectures: list[Lecture] = []

    class Config:
        orm_mode = True


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
        orm_mode = True
