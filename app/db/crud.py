import bcrypt
from typing import List, Union
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.exceptions import duplicate_pass
from app.db.models import UsersDatabaseModel
from app.security.security import get_password_hash


class CrudUsers:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @duplicate_pass
    async def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        city: str,
        address: str,
        phone: str,
        password: str) -> UsersDatabaseModel:
        password_hashed = get_password_hash(password)

        created_user = UsersDatabaseModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            city=city,
            address=address,
            phone=phone,
            password=password_hashed
        )
        self.db_session.add(created_user)
        await self.db_session.flush()
        return created_user

    async def get_users(self) -> List[UsersDatabaseModel]:
        sql = select(UsersDatabaseModel)
        query = await self.db_session.execute(sql)
        return query.scalars().all()

    async def get_user_by_uuid(self, uuid: Union[UUID, str]) -> UsersDatabaseModel:
        sql = select(UsersDatabaseModel).filter_by(id=uuid)
        query = await self.db_session.execute(sql)
        return query.scalar_one()

    async def get_user_by_email(self, email: str) -> UsersDatabaseModel:
        sql = select(UsersDatabaseModel).filter_by(email=email)
        query = await self.db_session.execute(sql)
        return query.scalar_one()
