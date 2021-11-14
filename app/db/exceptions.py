from asyncpg import UniqueViolationError
from ormar import NoMatch
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


def duplicate_pass(func):
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (IntegrityError, UniqueViolationError) as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail='The user with this email already exists in the system')

    return decorator


def no_match_pass(func):
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NoMatch:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail='The record you are looking for is missing from the database.')
    return decorator
