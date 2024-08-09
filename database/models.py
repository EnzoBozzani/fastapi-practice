from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Window(Base):
    __tablename__ = "windows"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    start = Column(String)
    end = Column(String)

    lectures = relationship("Lecture", back_populates="window")


class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    speaker_id = Column(Integer, ForeignKey("speakers.id"))
    window_id = Column(Integer, ForeignKey("windows.id"))

    speaker = relationship("Speaker", back_populates="lectures")
    window = relationship("Window", back_populates="lectures")


class Speaker(Base):
    __tablename__ = "speakers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    company = Column(String)
    linkedin = Column(String)
    image = Column(String)
    bio = Column(String)

    lectures = relationship("Lecture", back_populates="window")
