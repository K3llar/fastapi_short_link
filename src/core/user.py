import logging

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.db import get_async_session
from src.core.logger import LOG_FORMAT, LOG_NAME
from src.models.user import UserTable
from src.schemas.user import User, UserCreate, UserDB, UserUpdate

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_NAME,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(UserDB, session, UserTable)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def validate_password(
            self,
            password: str,
            user: UserCreate | UserDB
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
            self,
            user: UserDB,
            request: Request | None = None
    ) -> None:
        logger.info(f'User {user.email} registered')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_user = fastapi_users.current_user(active=True)
user_or_anon = fastapi_users.current_user(optional=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
