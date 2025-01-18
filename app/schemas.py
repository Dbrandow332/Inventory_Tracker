from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class InventoryItemBase(BaseModel):
    name: str
    count: int

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItem(BaseModel):
    id: int
    name: str
    count: int

    class Config:
        orm_mode = True

class InventoryItemUpdate(BaseModel):
    count: int

# Base schema for shared attributes
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True