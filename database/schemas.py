from pydantic import BaseModel, EmailStr, Field


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


class WindowBase(BaseModel):
    title: str = Field(min_length=3, max_length=250)
    start: str = Field(
        min_length=5, max_length=5, pattern="^([01]\d|2[0-3]):[0-5]\d$"
    )
    end: str = Field(
        min_length=5, max_length=5, pattern="^([01]\d|2[0-3]):[0-5]\d$"
    )


class WindowResponse(WindowBase):
    id: int


class WindowCreate(WindowBase):
    speaker_id: int | None
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


class SpeakerResponse(SpeakerBase):
    id: int


class Speaker(SpeakerBase):
    id: int
    lectures: list[Lecture] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
