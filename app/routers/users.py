from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.crud_users import create_user, get_users, update_user_me, delete_user_me
from app.schemas.user_schemas import (
    UserRegister,
    UserPublic,
    UserUpdate,
    UserInfoMe,
    UpdatePassword,
)
from app.database import get_db
from app.models import User
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


# POST /tasks
@router.post("/", response_model=UserPublic, status_code=201)
async def add_user(user: UserRegister, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)


# GET /users
@router.get("/", response_model=list[UserPublic])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)


@router.get("/me", response_model=UserInfoMe)
async def read_users_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


# PATCH /users/me
@router.patch("/me", response_model=UserPublic)
async def update_users_me(
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_user_me(db=db, user=current_user, user_data=user_data)


# DELETE /users/me
@router.delete("/me", status_code=204)
async def delete_users_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = await delete_user_me(db=db, user=current_user)
    return Response(status_code=204)
