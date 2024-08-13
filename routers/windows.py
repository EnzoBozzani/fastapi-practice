from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from database.schemas import WindowCreate, WindowResponse, WindowUpdate
from database.queries.window import create_window, get_windows, delete_window, update_window, get_windows_with_lectures_and_speakers  # noqa: E501
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
        dependencies=[Depends(get_user_by_token)]
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


@router.put(
    "/{id}",
    dependencies=[Depends(get_user_by_token)],
    response_model=WindowResponse
)
def update(id: int, windowUpdate: WindowUpdate):
    update_result = update_window(id, windowUpdate)

    if 'error' in update_result:
        return JSONResponse(
            status_code=update_result['status_code'],
            content={'error': update_result['error']}
        )

    return update_result['window']


@router.get("/lectures")
def get_with_lectures():
    return get_windows_with_lectures_and_speakers()
