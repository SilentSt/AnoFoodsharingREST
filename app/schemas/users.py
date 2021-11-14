from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


class BaseUserModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    role: int = Field(default=0)


class RegisterUserModel(BaseUserModel):
    password: Optional[str] = None


class BaseUserModelPatch(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    email: EmailStr = Field()
    city: str = Field(...)
    address: str = Field(...)
    phone: str = Field(...)
    role: int = Field(default=0)


class RegisterUserModelPatch(BaseUserModelPatch):
    password: str = Field(...)


class AuthUserModel(BaseUserModel):
    email: str
    password: str


class UserModel(BaseUserModel):
    id: UUID

