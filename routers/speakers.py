from fastapi import APIRouter, Depends, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import Annotated

from utils.main import save_file, delete_file
from utils.dependencies import get_user_by_token
from database.schemas import SpeakerCreate, SpeakerResponse, SpeakerUpdate
from database.queries.speaker import create_speaker, get_speakers, delete_speaker, update_speaker  # noqa: E501


router = APIRouter(
    prefix="/speaker",
    tags=["Speaker"]
)


@router.post(
        "",
        response_model=SpeakerResponse,
        dependencies=[Depends(get_user_by_token)]
)
async def create(
        image: UploadFile,
        name: Annotated[str, Form()],
        bio: Annotated[str, Form()],
        company: Annotated[str, Form()],
        linkedin: Annotated[str, Form()]
):
    speakerCreate = SpeakerCreate(
        name=name,
        bio=bio,
        linkedin=linkedin,
        company=company
    )

    speaker = create_speaker(speakerCreate)

    path = await save_file(speaker.id, image)

    speakerWithImage = SpeakerUpdate(image=path)

    updatedSpeaker = update_speaker(speaker.id, speakerWithImage)

    return updatedSpeaker


@router.get("", response_model=list[SpeakerResponse])
def get_all():
    return get_speakers()


@router.delete(
        "/{id}",
        dependencies=[Depends(get_user_by_token)],
        response_model=SpeakerResponse
)
def delete(id: int):
    speaker = delete_speaker(id)

    if speaker is not None:
        delete_file(speaker.image)

        return JSONResponse(
            status_code=200,
            content={'success': 'Deleted speaker successfully!'}
        )

    return JSONResponse(
            status_code=404,
            content={'error': 'Speaker not found!'}
        )


@router.put(
    "/{id}",
    response_model=SpeakerResponse,
    dependencies=[Depends(get_user_by_token)]
)
def update(id: int, speakerUpdate: SpeakerUpdate):
    speaker = update_speaker(id, speakerUpdate)

    if speaker is None:
        return JSONResponse(
            status_code=404,
            content={'error': 'Speaker not found!'}
        )

    return JSONResponse(
            status_code=200,
            content={'success': 'Updated speaker successfully!'}
        )
