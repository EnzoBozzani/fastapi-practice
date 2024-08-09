from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from database.queries import get_windows, create_window
from dependencies import get_db
from database.schemas import WindowCreate

router = APIRouter(
    prefix="/windows",
    tags=["Windows"],
)


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_windows(db)


@router.post("/")
def create(window: WindowCreate, db: Session = Depends(get_db)):
    return create_window(db, window)
