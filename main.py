import asyncpg
import uvicorn
from fastapi import FastAPI
from fastapi_asyncpg import configure_asyncpg
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.routes.binding import own_router
from app.routes.load import startup_handler, shutdown_handler
from misc import database
from settings import settings


def get_application() -> FastAPI:
    application = FastAPI(
        debug=True,
        docs_url='/docs',
        title='FoodSharing Microservice',
        version='0.0.1',
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=['*']
    )

    application.state.database = database

    application.add_event_handler("startup", startup_handler(application))
    application.add_event_handler("shutdown", shutdown_handler(application))
    application.include_router(own_router, prefix='/api/v1')
    return application


app = get_application()


if '__main__' == __name__:
    uvicorn.run("main:app", host="0.0.0.0", port=8021, reload=True, debug=True)
