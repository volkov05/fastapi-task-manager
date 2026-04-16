from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_db
from app.core.config import settings
from app.schemas.user_schemas import Token
from app.crud.crud_login import authenticate_user
from app.core.security import create_access_token

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@router.post("/", response_model=Token)
async def login_user(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    user = await authenticate_user(
        db=db, email=credentials.username, password=credentials.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(user.id, expires_delta=access_token_expires)
    )
