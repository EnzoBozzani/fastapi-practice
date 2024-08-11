from fastapi import APIRouter
from database.schemas import WindowCreate
from database.queries import create_window, get_windows

router = APIRouter(
    prefix="/windows",
    tags=["Windows"],
)


@router.get("/")
def get_all():
    return get_windows()


@router.post("/")
def create(window: WindowCreate):
    return create_window(window)
