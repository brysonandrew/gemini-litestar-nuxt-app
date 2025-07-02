from litestar import Litestar, get, post
from litestar.events import LifespanEvent

async def on_startup(app: Litestar) -> None:
    from database import create_db_and_tables
    create_db_and_tables()