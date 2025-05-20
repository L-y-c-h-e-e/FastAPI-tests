from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 1

    @field_validator('priority')
    def validate_priority(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Priority must be between 1 and 5')
        return v

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)