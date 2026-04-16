from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from datetime import datetime , timezone
import re

def is_valid_hex_color(v: str):
    if v and not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', v):
        raise ValueError("Hex color must be in the format #RRGGBB or #RGB")
    return v

# --- User Schemas ---
class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

# --- Category Schemas ---
class CategorySchema(BaseModel):
    name: str = Field(..., min_length=1)
    color: str = Field(default="#000000")
    user_id: str 

    @field_validator('color')
    @classmethod
    def validate_color(cls, v):
        return is_valid_hex_color(v)

# --- Subtask Schemas ---
class SubtaskSchema(BaseModel):
    title: str = Field(..., min_length=1)
    is_done: bool = False

# --- Task Schemas ---
class TaskCreateSchema(BaseModel):
    user_id: str = Field(...) 
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = ""
    priority: int = Field(default=3, ge=1, le=5) 
    due_date: Optional[datetime] = None
    category_id: Optional[str] = None 
    subtasks: List[SubtaskSchema] = []

    @field_validator('due_date')
    @classmethod
    def date_must_be_future(cls, v):
        if v and v < datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future")
        return v

class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = None 
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[datetime] = None
    category_id: Optional[str] = None
    subtasks: Optional[List[SubtaskSchema]] = None