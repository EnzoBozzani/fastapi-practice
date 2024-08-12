from fastapi import APIRouter

from database.schemas import WindowCreate, WindowResponse
from database.queries import create_window, get_windows

router = APIRouter(
    prefix="/windows",
    tags=["Windows"],
)


@router.get("/", response_model=list[WindowResponse])
def get_all():
    return get_windows()


@router.post("/", response_model=WindowResponse)
def create(window: WindowCreate):
    return create_window(window)
