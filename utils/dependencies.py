import jwt
import os
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from database.schemas import TokenData
from database.queries import get_admin


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_user_by_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token, os.environ['JWT_SECRET'],
            algorithms=[os.environ['JWT_ALGORITHM']]
        )
        username: str = payload.get('sub')

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = get_admin(token_data.username or "")

    if user is None:
        raise credentials_exception

    return user
