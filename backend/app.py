from typing import Any, Dict
from litestar import Litestar, get, post
from litestar.di import Provide
from litestar.connection import ASGIConnection, Request
from litestar.security.jwt import JWTAuth, Token
from litestar.dto import DTOConfig
from litestar.plugins.pydantic import PydanticDTO
from pydantic import BaseModel
import uvicorn
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from litestar.exceptions import HTTPException
from traceback import format_exc
from database import SessionLocal, User as DBUser

from litestar.exceptions import NotAuthorizedException
from database import get_db, User as DBUser

import logging

logging.basicConfig(level=logging.INFO)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    id: int
    name: str
    email: str


class LoginData(BaseModel):
    email: str
    password: str


class RegisterData(BaseModel):
    name: str
    email: str
    password: str


class LoginDTO(PydanticDTO[LoginData]):
    config = DTOConfig()



async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User | None:
    db = SessionLocal()
    try:
        user = db.query(DBUser).filter(DBUser.id == int(token.sub)).first()
        if user:
            return User(id=user.id, name=user.name, email=user.email)
        return None
    finally:
        db.close()

jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret="super-secret-key-that-is-long-and-secure",
    exclude=["/login", "/register"],
)


@post("/login", dto=LoginDTO)
async def login(data: LoginData, db: Session = Provide(get_db)) -> Dict[str, str]:
    user = db.query(DBUser).filter(DBUser.email == data.email).first()
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise NotAuthorizedException("Invalid credentials")

    token = jwt_auth.create_token(str(user.id))
    return {"token": token}


@post("/register")
async def register(data: RegisterData, db: Session = Provide(get_db)) -> Dict[str, str]:
    logging.info(f"Registering user: {data}")

    try:
        hashed_password = pwd_context.hash(data.password)
        new_user = DBUser(
            name=data.name, email=data.email, hashed_password=hashed_password
        )
        logging.info(f"New user: {new_user}")

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = jwt_auth.create_token(str(new_user.id))
        logging.info(f"Token created: {token}")
        return {"token": token}

    except IntegrityError as e:
        db.rollback()
        logging.error("IntegrityError:", exc_info=e)
        raise HTTPException(status_code=400, detail="Email already exists")

    except Exception as e:
        db.rollback()
        logging.error("Unexpected error during registration:")
        logging.error(format_exc())  # Print full traceback
        raise HTTPException(status_code=500, detail="Internal server error")

@get("/profile")
async def get_profile(request: Request) -> User:
    logging.info("HELLO")
    logging.error(format_exc())  # Print full traceback

    try:
        logging.info(f"request.user: {request.user}")
        if not request.user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return request.user
    except Exception:
        logging.error("Error in /profile:")
        logging.error(format_exc())  # log full traceback
        raise HTTPException(status_code=500, detail="Internal server error")


from litestar.config.cors import CORSConfig

cors_config = CORSConfig(
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True,
)

async def on_startup(app: Litestar) -> None:
    from database import create_db_and_tables
    create_db_and_tables()


app = Litestar(
    route_handlers=[login, register, get_profile],
    on_app_init=[jwt_auth.on_app_init],
    on_startup=[on_startup],
    cors_config=cors_config,
    dependencies={"db": Provide(get_db)},
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
