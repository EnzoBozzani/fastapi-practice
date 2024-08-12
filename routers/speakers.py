from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from utils.dependencies import get_user_by_token
from database.schemas import SpeakerCreate, SpeakerResponse
from database.queries.speaker import create_speaker, get_speakers, delete_speaker  # noqa: E501


router = APIRouter(
    prefix="/speaker",
    tags=["Speaker"]
)


@router.post(
        "/",
        response_model=SpeakerResponse,
        dependencies=[Depends(get_user_by_token)]
)
def create(speaker: SpeakerCreate):
    return create_speaker(speaker)


@router.get("/", response_model=list[SpeakerResponse])
def get_all():
    return get_speakers()


@router.delete(
        "/{id}",
        dependencies=[Depends(get_user_by_token)],
        response_model=SpeakerResponse
)
def delete(id: int):
    deleted = delete_speaker(id)

    if deleted:
        return JSONResponse(
            status_code=200,
            content={'success': 'Deleted speaker successfully!'}
        )

    return JSONResponse(
            status_code=404,
            content={'error': 'Speaker not found!'}
        )
