from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.schemas.task import TaskResponse


class TimeLogCreate(BaseModel):
    task_id: int = Field(..., description="ID задачи")
    minutes: int = Field(..., gt=0, description="Количество минут (больше 0)")
    comment: Optional[str] = Field(None, max_length=500, description="Комментарий")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 1,
                "minutes": 120,
                "comment": "Работал над функцией создания задач"
            }
        }


class TimeLogResponse(BaseModel):
    id: int
    task_id: int
    minutes: int
    comment: Optional[str]
    logged_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
        
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "task_id": 1,
                "minutes": 120,
                "comment": "Работал над функцией создания задач",
                "logged_at": "2024-01-01T12:00:00",
                "created_at": "2024-01-01T12:00:00"
            }
        }


class TimeLogWithTask(TimeLogResponse):
    task: TaskResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "task_id": 1,
                "minutes": 120,
                "comment": "Работал над функцией создания задач",
                "logged_at": "2024-01-01T12:00:00",
                "created_at": "2024-01-01T12:00:00",
                "task": {
                    "id": 1,
                    "user_id": 12345,
                    "title": "Изучить FastAPI",
                    "status": "active",
                    "created_at": "2024-01-01T10:00:00"
                }
            }
        }
