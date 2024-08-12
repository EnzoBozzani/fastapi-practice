from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from database.schemas import WindowCreate, WindowResponse
from database.queries.window import create_window, get_windows, delete_window
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


@router.delete(
        "/{id}",
        dependencies=[Depends(get_user_by_token)],
        response_model=WindowResponse
)
def delete(id: int):
    deleted = delete_window(id)

    if deleted:
        return JSONResponse(
            status_code=200,
            content={'success': 'Deleted window successfully!'}
        )

    return JSONResponse(
            status_code=404,
            content={'error': 'Window not found!'}
        )
