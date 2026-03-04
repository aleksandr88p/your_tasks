from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from typing import List, Optional

from app.core.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskStatusUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate, 
    telegram_user_id: int = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Создать новую задачу"""
    db_task = Task(title=task.title, user_id=telegram_user_id)
    
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    
    return db_task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    telegram_user_id: int = Header(...),
    status: Optional[str] = Query(None, description="Фильтр по статусу (active/completed)"),
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех задач пользователя с опциональной фильтрацией по статусу"""
    query = select(Task).where(Task.user_id == telegram_user_id)
    
    if status:
        query = query.where(Task.status == status)
    
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    telegram_user_id: int = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Получить задачу по ID"""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == telegram_user_id)
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return task


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    status_update: TaskStatusUpdate,
    telegram_user_id: int = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Изменить статус задачи"""
    result = await db.execute(
        select(Task).where(and_(Task.id == task_id, Task.user_id == telegram_user_id))
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    task.status = status_update.status.value
    await db.commit()
    await db.refresh(task)
    
    return task
