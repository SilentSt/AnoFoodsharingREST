from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from starlette.responses import JSONResponse, Response, FileResponse
from uuid import UUID
from app.db.crud import CrudDatabase
from app.schemas.tasks import AddressModel
from app.schemas.users import RegisterUserModel, UserModel
from app.security.auth import get_current_user
from app.utils.pdfsaver import generate_path_file, chunked_copy

tasks_router = APIRouter()


# @tasks_router.get('/tasks')
# async def get_all_tasks(
#     db: CrudDatabase = Depends(CrudDatabase)
# ):
#
#     sql = await db.get_all_addresses()
#     print(sql)
#     # data = {"detail": "User created", "uuid": str(sql.id)}
#     return JSONResponse(status_code=200, content=sql)
#
#

@tasks_router.get('/volunteering/address', summary='Посмотреть все адреса.')
async def get_all_tasks(
    db: CrudDatabase = Depends(CrudDatabase)
):
    return await db.get_all_addresses()


@tasks_router.get('/volunteering/schedule', summary='Посмотреть полное расписание доставок для всех задач')
async def org_rec(
    db: CrudDatabase = Depends(CrudDatabase)
):
    return await db.get_all_organizations_recipients()


@tasks_router.post('/volunteering/delivery/{delivery_id}', summary='Изменить статус доставки для задачи')
async def execute_delivery_by_id(
    delivery_id: int,
    file: UploadFile = File(...),
    db: CrudDatabase = Depends(CrudDatabase),

):

    """
    Передаем файл PDF, после этого меняем статус задачи на доставлено.
    """
    file_path = generate_path_file(filename=file.filename)
    await db.update_delivery_path_status_by_id(delivery_id=delivery_id, document_path=file_path)
    await chunked_copy(src=file, dst=file_path)

    return JSONResponse(status_code=200, content={"content": "PDF was loaded successfully"})


@tasks_router.get('/documents/delivery/{file_id}.pdf', summary='Получить фотографию по айди.')
async def foo(
    file_id: str,
    db: CrudDatabase = Depends(CrudDatabase),

):
    """
    Получаем PDF, добавленный ранее.
    """

    photo_url = await db.get_document_path(document_id=file_id)
    return FileResponse(path=photo_url)


