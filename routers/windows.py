from fastapi import APIRouter, Depends

from database.schemas import WindowCreate, WindowResponse
from database.queries import create_window, get_windows
from utils.dependencies import get_user_by_token

router = APIRouter(
    prefix="/windows",
    tags=["Windows"],
)


@router.get("/", response_model=list[WindowResponse])
def get_all():
    return get_windows()


@router.post(
        "/",
        response_model=WindowResponse,
        dependencies=[Depends(get_user_by_token)]
)
def create(window: WindowCreate):
    return create_window(window)
