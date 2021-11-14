from typing import List
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from uuid import UUID
from app.db.crud import CrudDatabase
from app.schemas.users import RegisterUserModel, UserModel, RegisterUserModelPatch
from app.security.auth import get_current_user

users_router = APIRouter()


@users_router.post('/users')
async def create_user(
    data: RegisterUserModelPatch,
    db: CrudDatabase = Depends(CrudDatabase)
):

    sql = await db.create_user(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        city=data.city,
        address=data.address,
        phone=data.phone,
        password=data.password
    )
    data = {"detail": "User created", "uuid": str(sql.id)}
    return JSONResponse(status_code=201, content=data)


@users_router.get('/users', response_model=List[UserModel])
async def get_users(
    db: CrudDatabase = Depends(CrudDatabase)
):
    return await db.get_users()


@users_router.get('/users/{user_id}', response_model=UserModel)
async def get_user(
    user_id: UUID,
    db: CrudDatabase = Depends(CrudDatabase)):
    sql = await db.get_user_by_uuid(user_id)
    return sql


@users_router.patch('/users/{user_id}')
async def update_user(
    user_id: UUID,
    data: RegisterUserModel,
    db: CrudDatabase = Depends(CrudDatabase)):

    contract_dict = data.dict(exclude_none=True)
    await db.patch_user(uuid=user_id, **contract_dict)

    return JSONResponse(status_code=200, content={"content": "Data changed"})


@users_router.get("/me", response_model=UserModel)
def read_users_me(current_user: CrudDatabase = Depends(get_current_user)):

    user = current_user
    return user
