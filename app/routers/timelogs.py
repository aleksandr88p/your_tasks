from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from typing import List

from app.core.database import get_db
from app.models.timelog import TimeLog
from app.models.task import Task
from app.schemas.timelog import TimeLogCreate, TimeLogResponse, TimeLogWithTask

router = APIRouter(prefix="/timelogs", tags=["timelogs"])


@router.post("/", response_model=TimeLogResponse)
async def create_timelog(
    timelog: TimeLogCreate,
    telegram_user_id: int = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Добавить время к задаче"""
    # Проверяем, что задача принадлежит пользователю
    task_result = await db.execute(
        select(Task).where(and_(Task.id == timelog.task_id, Task.user_id == telegram_user_id))
    )
    task = task_result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена или не принадлежит вам")
    
    db_timelog = TimeLog(
        task_id=timelog.task_id,
        minutes=timelog.minutes,
        comment=timelog.comment
    )
    
    db.add(db_timelog)
    await db.commit()
    await db.refresh(db_timelog)
    
    return db_timelog


@router.get("/", response_model=List[TimeLogWithTask])
async def get_timelogs(
    telegram_user_id: int = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Получить все логи времени пользователя"""
    result = await db.execute(
        select(TimeLog).join(Task).where(Task.user_id == telegram_user_id)
    )
    timelogs = result.scalars().all()
    
    # Конвертируем SQLAlchemy модели в Pydantic с помощью from_attributes
    timelogs_with_tasks = []
    for timelog in timelogs:
        await db.refresh(timelog, ["task"])
        timelogs_with_tasks.append(TimeLogWithTask.model_validate(timelog, from_attributes=True))
    
    return timelogs_with_tasks


@router.get("/task/{task_id}", response_model=List[TimeLogResponse])
async def get_task_timelogs(
    task_id: int,
    telegram_user_id: int = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Получить логи времени по конкретной задаче"""
    # Проверяем, что задача принадлежит пользователю
    task_result = await db.execute(
        select(Task).where(and_(Task.id == task_id, Task.user_id == telegram_user_id))
    )
    task = task_result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена или не принадлежит вам")
    
    result = await db.execute(
        select(TimeLog).where(TimeLog.task_id == task_id)
    )
    timelogs = result.scalars().all()
    
    return timelogs
