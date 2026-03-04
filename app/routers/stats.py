from fastapi import APIRouter, Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, case
from typing import Optional

from app.core.database import get_db
from app.models.task import Task
from app.models.timelog import TimeLog
from app.schemas.stats import StatsSummary, TaskStats

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary", response_model=StatsSummary)
async def get_stats_summary(
    telegram_user_id: int = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Получить общую статистику пользователя"""
    
    # Считаем задачи по статусам
    tasks_result = await db.execute(
        select(
            func.count(Task.id).label('total_tasks'),
            func.sum(case((Task.status == 'active', 1), else_=0)).label('active_tasks'),
            func.sum(case((Task.status == 'completed', 1), else_=0)).label('completed_tasks')
        ).where(Task.user_id == telegram_user_id)
    )
    tasks_stats = tasks_result.first()
    
    # Считаем общее время
    time_result = await db.execute(
        select(func.sum(TimeLog.minutes).label('total_minutes'))
        .join(Task).where(Task.user_id == telegram_user_id)
    )
    total_minutes = time_result.scalar() or 0
    
    # Среднее время на задачу (только по задачам с логами)
    avg_result = await db.execute(
        select(func.avg(TimeLog.minutes).label('avg_minutes'))
        .join(Task).where(Task.user_id == telegram_user_id)
    )
    avg_minutes = avg_result.scalar() or 0
    
    return StatsSummary(
        total_tasks=tasks_stats.total_tasks or 0,
        active_tasks=tasks_stats.active_tasks or 0,
        completed_tasks=tasks_stats.completed_tasks or 0,
        total_minutes=total_minutes,
        avg_minutes_per_task=float(avg_minutes)
    )


@router.get("/tasks/{task_id}", response_model=TaskStats)
async def get_task_stats(
    task_id: int,
    telegram_user_id: int = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """Получить статистику по конкретной задаче"""
    
    # Проверяем, что задача принадлежит пользователю
    task_result = await db.execute(
        select(Task).where(and_(Task.id == task_id, Task.user_id == telegram_user_id))
    )
    task = task_result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Считаем статистику по времени
    stats_result = await db.execute(
        select(
            func.sum(TimeLog.minutes).label('total_minutes'),
            func.count(TimeLog.id).label('log_count'),
            func.max(TimeLog.logged_at).label('last_log_date')
        ).where(TimeLog.task_id == task_id)
    )
    stats = stats_result.first()
    
    return TaskStats(
        task_id=task.id,
        task_title=task.title,
        task_status=task.status,
        total_minutes=stats.total_minutes or 0,
        log_count=stats.log_count or 0,
        last_log_date=stats.last_log_date
    )
