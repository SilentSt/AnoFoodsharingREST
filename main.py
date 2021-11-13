import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.routes.binding import own_router


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

    application.include_router(own_router, prefix='/api/v1')

    return application


app = get_application()


if '__main__' == __name__:
    uvicorn.run("main:app", host="0.0.0.0", port=8021, reload=True, debug=True)
