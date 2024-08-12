from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from utils.dependencies import get_user_by_token
from database.schemas import LectureCreate, LectureResponse
from database.queries.lecture import create_lecture, get_lectures, delete_lecture  # noqa: E501


router = APIRouter(
    prefix="/lecture",
    tags=["Lecture"]
)


@router.post(
        "/",
        response_model=LectureResponse,
        dependencies=[Depends(get_user_by_token)]
)
def create(lecture: LectureCreate):
    return create_lecture(lecture)


@router.get("/", response_model=list[LectureResponse])
def get_all():
    return get_lectures()


@router.delete(
        "/{id}",
        dependencies=[Depends(get_user_by_token)],
        response_model=LectureResponse
)
def delete(id: int):
    deleted = delete_lecture(id)

    if deleted:
        return JSONResponse(
            status_code=200,
            content={'success': 'Deleted lecture successfully!'}
        )

    return JSONResponse(
            status_code=404,
            content={'error': 'Lecture not found!'}
        )
