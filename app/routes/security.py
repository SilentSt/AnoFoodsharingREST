from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.db.crud import CrudDatabase
from app.security.auth import authenticate, create_access_token

security_router = APIRouter()


@security_router.post("/login")
async def login(
    db: CrudDatabase = Depends(CrudDatabase),
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = await authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }
