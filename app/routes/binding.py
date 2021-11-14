from fastapi import APIRouter

from app.routes.tasks import tasks_router
from app.routes.users import users_router
from app.routes.security import security_router
from app.routes.parsers import file_router

own_router = APIRouter()

own_router.include_router(users_router, tags=['Users'])
own_router.include_router(security_router, tags=['Security'])
own_router.include_router(tasks_router, tags=['Tasks'])
own_router.include_router(file_router, tags=['Documents'], prefix='/parsers')