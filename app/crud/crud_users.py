import uuid
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models import User
from app.schemas.user_schemas import UserRegister, UserUpdate
from app.core.security import get_password_hash


async def create_user(db: AsyncSession, user_create: UserRegister):
    user_data = user_create.model_dump()
    user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    new_user = User(**user_data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_users(db: AsyncSession):
    results = await db.execute(select(User))
    return results.scalars().all()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def update_user_me(db: AsyncSession, user: User, user_data: UserUpdate):
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided")
    for field, value in update_data.items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user_me(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()
