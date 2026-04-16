import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# Базовая схема
class TaskBase(BaseModel):
    description: str
    status: bool = False
    deadline: Optional[datetime] = None
    created_at: Optional[datetime] = None


# Схема для создания задачи
class TaskCreate(TaskBase):
    pass


# Схема для обновления задачи
class TaskUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[bool] = None
    deadline: Optional[datetime] = None


# Схемы для чтения задачи (для response_model)
class TaskPublic(TaskBase):
    id: uuid.UUID
    owner_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
