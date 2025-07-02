from typing import Dict

from litestar import post
from litestar.di import Provide
from litestar.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from traceback import format_exc
import logging

from auth import jwt_auth, pwd_context
from database import get_db, User as DBUser
from schemas import RegisterData


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
