from fastapi import APIRouter, Depends

from utils.dependencies import get_user_by_token
from database.schemas import SpeakerCreate, SpeakerResponse
from database.queries.speaker import create_speaker, get_speakers


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
