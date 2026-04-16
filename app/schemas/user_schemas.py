import uuid
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


# Схема для создания пользователя
class UserRegister(BaseModel):
    email: EmailStr
    password: str


# Схема для ответа данных
class UserPublic(BaseModel):
    id: uuid.UUID
    email: EmailStr
    login: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserInfoMe(BaseModel):
    email: EmailStr
    login: Optional[str] = None
    created_at: datetime


# Схема для обновления данных
class UserUpdate(BaseModel):
    login: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = ConfigDict(extra="forbid")


# Схема смены пароля
class UpdatePassword(BaseModel):
    current_password: str
    new_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# JSON-данные, содержащие токен доступа
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: Optional[str] = None
