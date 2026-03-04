from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class StatsSummary(BaseModel):
    total_tasks: int = Field(..., description="Общее количество задач")
    active_tasks: int = Field(..., description="Количество активных задач")
    completed_tasks: int = Field(..., description="Количество завершенных задач")
    total_minutes: int = Field(..., description="Общее время в минутах")
    avg_minutes_per_task: float = Field(..., description="Среднее время на задачу")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_tasks": 10,
                "active_tasks": 7,
                "completed_tasks": 3,
                "total_minutes": 1200,
                "avg_minutes_per_task": 120.0
            }
        }


class TaskStats(BaseModel):
    task_id: int = Field(..., description="ID задачи")
    task_title: str = Field(..., description="Название задачи")
    task_status: str = Field(..., description="Статус задачи")
    total_minutes: int = Field(..., description="Общее время по задаче в минутах")
    log_count: int = Field(..., description="Количество логов времени")
    last_log_date: Optional[datetime] = Field(None, description="Дата последнего лога")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 1,
                "task_title": "Изучить FastAPI",
                "task_status": "active",
                "total_minutes": 240,
                "log_count": 3,
                "last_log_date": "2024-01-01T15:30:00"
            }
        }
