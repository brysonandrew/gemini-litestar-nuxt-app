from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth, Token
from passlib.context import CryptContext

from database import SessionLocal, User as DBUser
from schemas import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
