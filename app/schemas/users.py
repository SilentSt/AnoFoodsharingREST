from pydantic import BaseModel
from uuid import UUID


class BaseUserModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    city: str
    address: str
    phone: str

    class Config:
        orm_mode = True


class RegisterUserModel(BaseUserModel):
    password: str


class AuthUserModel(BaseUserModel):
    email: str
    password: str


class UserModel(BaseUserModel):
    id: UUID

