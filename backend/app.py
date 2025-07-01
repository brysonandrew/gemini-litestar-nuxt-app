
from typing import Any, Dict
from litestar import Litestar, get, post, Request
from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth, Token
from litestar.dto import DTOConfig
from litestar.plugins.pydantic import PydanticDTO
from pydantic import BaseModel
import uvicorn

from litestar.exceptions import NotAuthorizedException

class User(BaseModel):
    id: int
    name: str
    email: str

class LoginData(BaseModel):
    email: str
    password: str

class LoginDTO(PydanticDTO[LoginData]):
    config = DTOConfig()

users = {
    1: User(id=1, name="John Doe", email="john.doe@example.com")
}

async def retrieve_user_handler(token: Token, connection: ASGIConnection[Any, Any, Any, Any]) -> User | None:
    user = users.get(int(token.sub))
    return user

jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret="super-secret-key-that-is-long-and-secure",
    exclude=["/login"]
)

@post("/login", dto=LoginDTO)
async def login(data: LoginData) -> Dict[str, str]:
    # In a real app, you'd validate the password here
    
    user = next((user for user in users.values() if user.email == data.email), None)
    if not user:
        raise NotAuthorizedException("Invalid credentials")
    
    token = jwt_auth.create_token(str(user.id))
    return {"token": token}

@get("/profile")
def get_profile(request: Request[User, Token, Any]) -> User:
    return request.user

from litestar.config.cors import CORSConfig

cors_config = CORSConfig(
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True,
)

app = Litestar(
    route_handlers=[login, get_profile],
    on_app_init=[jwt_auth.on_app_init],
    cors_config=cors_config,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
