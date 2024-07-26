from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import sys

sys.path.append('src')

from app.multipart.schemas.token import TokenScheme
from app.multipart.schemas.user import UserLoginScheme
from app.multipart.models.user import User
from app.multipart.utils.auth import verify_password, decode_acces_token
from app.multipart.connection.cache import cache_redis


async def authenticate_user(session: AsyncSession, user_login_form: UserLoginScheme) -> User | None:
    '''Аутентификация пользоваетля.'''
    result = await session.execute(select(User).where(User.email == user_login_form.email))  # Сверяем по логину
    user = result.scalar()
    if user:
       if verify_password(user_login_form.password, user.hashed_password):  # Проверяем пароль
           return user


async def get_current_user(session: AsyncSession, token: TokenScheme) -> User | None:
    '''Получение текущего пользователя по токену'''
    token_data = decode_acces_token(token=token)
    user_token: str | None = await cache_redis.get(str(token_data.id_user))  # Проверяем есть ли токен в кэше
    if user_token:
        if user_token == token.token:  # Сверяем его ли токен
            result = await session.execute(select(User).where(User.id == token_data.id_user)) 
            return result.scalar()  # В случае учпеха отдаем пользователя
    else:
        result = await session.execute(select(User).where(User.token == token.token))  # Иначе ищем токен в БД
        user = result.scalar()
        if token_data and user:
            user_id = token_data.id_user  # Сверяем его ли токен
            if user_id == user.id:
                return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )


async def get_current_active_user(session: AsyncSession, token: TokenScheme) -> User | None:
    '''Получение текущего пользователя (с проверкой на бан)'''
    user = await get_current_user(session=session, token=token)
    if user:
        if user.disabled:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied",
        )
        return user
    