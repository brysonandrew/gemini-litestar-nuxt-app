from typing import Dict

from litestar import post
from litestar.di import Provide
from litestar.exceptions import NotAuthorizedException
from sqlalchemy.orm import Session

from auth import jwt_auth, pwd_context
from database import get_db, User as DBUser
from schemas import LoginDTO, LoginData


@post("/login", dto=LoginDTO)
async def login(data: LoginData, db: Session = Provide(get_db)) -> Dict[str, str]:
    user = db.query(DBUser).filter(DBUser.email == data.email).first()
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise NotAuthorizedException("Invalid credentials")

    token = jwt_auth.create_token(str(user.id))
    return {"token": token}
