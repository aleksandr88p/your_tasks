from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    active = "active"
    completed = "completed"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Название задачи")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Изучить FastAPI"
            }
        }


class TaskStatusUpdate(BaseModel):
    status: TaskStatus = Field(..., description="Новый статус задачи")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "completed"
            }
        }


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "title": "Изучить FastAPI",
                "status": "active",
                "created_at": "2024-01-01T12:00:00"
            }
        }
