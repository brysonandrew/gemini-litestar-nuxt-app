from litestar import Litestar
from litestar.di import Provide
from litestar.config.cors import CORSConfig
import uvicorn

from auth import jwt_auth
from database import get_db
from routes.login import login
from routes.register import register
from routes.profile import get_profile


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