from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from database.schemas import WindowCreate, WindowResponse
from database.queries.window import create_window, get_windows
from utils.dependencies import get_user_by_token

router = APIRouter(
    prefix="/windows",
    tags=["Window"],
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
    created = create_window(windowCreate=window)

    if created:
        return created

    return JSONResponse(
        status_code=400,
        content={'error': 'Time collision detected with existing window!'}
    )
