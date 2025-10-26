from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class SubcategoryBase(BaseModel):
    title: str
    details: Optional[str] = ''
    progress: Optional[int] = 0
    due_date: Optional[datetime] = None

class SubcategoryCreate(SubcategoryBase):
    pass

class SubcategoryOut(SubcategoryBase):
    id: int
    notified: bool
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = ''

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    owner_email: str
    archived: bool
    subcategories: List[SubcategoryOut] = []
    class Config:
        orm_mode = True

class NotificationOut(BaseModel):
    id: int
    subcategory_id: int
    message: str
    created_at: datetime
    class Config:
        orm_mode = True
