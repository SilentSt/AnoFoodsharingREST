from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


def duplicate_pass(func):
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail='The user with this email already exists in the system')

    return decorator


def no_match_pass(func):
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail='The record you are looking for is missing from the database.')
    return decorator
