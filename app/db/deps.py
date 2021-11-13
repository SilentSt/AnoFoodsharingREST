from app.db.crud import CrudUsers
from misc import async_session


async def get_crud_users():
    async with async_session() as session:
        async with session.begin():
            yield CrudUsers(session)
