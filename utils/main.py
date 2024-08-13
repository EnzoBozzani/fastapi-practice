import jwt
import os
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from fastapi import UploadFile

from database.schemas import WindowWithLectures
from database.models import Window

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        os.environ['JWT_SECRET'],
        algorithm=os.environ['JWT_ALGORITHM']
    )
    return encoded_jwt


def check_for_time_collision(windows: list[Window], current: Window):
    current_start_hour = float(current.start.split(':')[0])
    current_start_min = float(current.start.split(':')[1])
    current_end_hour = float(current.end.split(':')[0])
    current_end_min = float(current.end.split(':')[1])

    current_interval = [
        current_start_hour + (current_start_min/60),
        current_end_hour + (current_end_min/60)
    ]

    for window in windows:
        start_hour = float(window.start.split(':')[0])
        start_min = float(window.start.split(':')[1])
        end_hour = float(window.end.split(':')[0])
        end_min = float(window.end.split(':')[1])

        interval = [start_hour + (start_min/60), end_hour + (end_min/60)]

        if (
            (
                current_interval[0] > interval[0]
                and
                current_interval[0] < interval[1])
            or
            (
                current_interval[1] > interval[0]
                and
                current_interval[1] < interval[1]
            )
        ):
            return True

    return False


async def save_file(id: int, uploadFile: UploadFile):
    file_extension = uploadFile.content_type.split("/")[1] if uploadFile.content_type is not None else "jpeg"  # noqa: E501
    with open(f'./public/{id}.{file_extension}', 'wb') as f:
        buffer = await uploadFile.read()
        f.write(buffer)

        return f'/{id}.{file_extension}'


def delete_file(imgUrl: str):
    os.remove(f'./public{imgUrl}')


def get_index(list: list[WindowWithLectures], window: Window):
    index = 0
    for w in list:
        if w.id == window.id:
            return index
        index += 1

    return None
