from litestar import get
from litestar.connection import Request
from litestar.exceptions import HTTPException
from traceback import format_exc
import logging

from schemas import User


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
