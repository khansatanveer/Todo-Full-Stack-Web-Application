from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from datetime import datetime
import uuid

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def password_byte_length(cls, v: str) -> str:
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password must be 72 bytes or less (some characters use multiple bytes)')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def password_byte_length(cls, v: str) -> str:
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password must be 72 bytes or less')
        return v

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)