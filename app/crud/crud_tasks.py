import uuid
from re import search
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate


# Создать задачу
async def create_task(
    db: AsyncSession, task_data: TaskCreate, owner_id: uuid.UUID
) -> Task:
    new_task = Task(**task_data.model_dump(), owner_id=owner_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


# Получить все задачи пользователя
async def get_tasks(
    db: AsyncSession,
    owner_id: uuid.UUID,
    skip: int,
    limit: int,
    search_query: Optional[str],
):
    stmt = select(Task).where(Task.owner_id == owner_id)
    if search_query:
        stmt = stmt.where(Task.description.ilike(f"%{search_query}%"))
    stmt = stmt.order_by(Task.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# Получить задачу по ID
async def get_task_id(
    db: AsyncSession, task_id: uuid.UUID, owner_id: uuid.UUID
) -> Task | None:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
    )
    return result.scalar_one_or_none()


# Обновить задачу
async def update_task(
    db: AsyncSession, task_id: uuid.UUID, task_data: TaskUpdate, owner_id: uuid.UUID
) -> Task | None:
    task = await get_task_id(db, task_id, owner_id)
    if not task:
        return None
    for field_name, new_value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field_name, new_value)
    await db.commit()
    await db.refresh(task)
    return task


# Удалить задачу (только если принадлежит пользователю)
async def delete_task(
    db: AsyncSession, task_id: uuid.UUID, owner_id: uuid.UUID
) -> bool:
    task = await get_task_id(db, task_id, owner_id)
    if not task:
        return False
    await db.delete(task)
    await db.commit()
    return True
