from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.crud.crud_users import get_user_by_email
from app.core.security import verify_password

DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$C7uWk...example"


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user:
        verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        user.hashed_password = updated_password_hash
        await db.commit()
        await db.refresh(user)
    return user
