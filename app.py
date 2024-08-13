from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from routers import windows, speakers, lectures
from database.schemas import Token, AdminCreate
from database.queries.admin import authenticate_admin, add_admin
from utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.main import create_access_token

load_dotenv()


app = FastAPI()


app.include_router(windows.router)
app.include_router(speakers.router)
app.include_router(lectures.router)


app.mount("/", StaticFiles(directory="public"), name="public")


@app.post('/login', response_model=Token, tags=["Admin"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_admin(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="Bearer")


@app.post('/add-admin', tags=["Admin"])
def create_admin(adminCreate: AdminCreate):
    new_admin = add_admin(
        email=adminCreate.email,
        password=adminCreate.password
    )

    if new_admin is None:
        return JSONResponse(
            status_code=400,
            content={'error': f'Admin ${adminCreate.email} already exists!'}
        )

    return JSONResponse(
        status_code=200,
        content={'success': 'Created new admin!'}
    )
