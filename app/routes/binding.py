from fastapi import APIRouter

from app.routes.users import users_router
from app.routes.security import security_router

own_router = APIRouter()

own_router.include_router(users_router, tags=['Users'])
own_router.include_router(security_router, tags=['Security'])