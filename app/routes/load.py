from typing import Callable

import asyncpg
from fastapi import FastAPI


def startup_handler(app: FastAPI) -> Callable:
    async def startup() -> None:
        database_ = app.state.database
        if not database_.is_connected:
            await database_.connect()

    return startup


def shutdown_handler(app: FastAPI) -> Callable:
    async def shutdown() -> None:
        database_ = app.state.database
        if database_.is_connected:
            await database_.disconnect()
    return shutdown
