import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.crud_tasks import (
    get_tasks,
    get_task_id,
    create_task,
    update_task,
    delete_task,
)
from app.core.security import get_current_user
from app.models import User
from app.models import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskPublic
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


# POST /tasks
@router.post("/", response_model=TaskPublic, status_code=201)
async def add_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_task(db=db, task_data=task, owner_id=current_user.id)


# GET /tasks
@router.get("/", response_model=list[TaskPublic])
async def read_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    search_query: Optional[str] = None,
):
    return await get_tasks(
        db, owner_id=current_user.id, skip=skip, limit=limit, search_query=search_query
    )


# GET /tasks/{task_id}
@router.get("/{task_id}", response_model=TaskPublic)
async def read_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await get_task_id(db, task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(
            status_code=404, detail=f"Task with id: {task_id} not found"
        )
    return task


# PATCH /tasks/{task_id}
@router.patch("/{task_id}", response_model=TaskUpdate)
async def edit_task(
    task_id: uuid.UUID,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await update_task(db, task_id, task_data, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# DELETE /tasks/{task_id}
@router.delete("/{task_id}", status_code=204)
async def remove_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = await delete_task(db, task_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=404, detail=f"Task with id: {task_id} does not exist"
        )
    return Response(status_code=204)
