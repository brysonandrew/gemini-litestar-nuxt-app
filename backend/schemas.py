from litestar.dto import DTOConfig
from litestar.plugins.pydantic import PydanticDTO
from pydantic import BaseModel


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
