from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

import sys

sys.path.append('src')

from app.multipart.crud.service import authenticate_user, get_current_user
from app.multipart.schemas.token import TokenDataScheme, TokenScheme
from app.multipart.schemas.user import UserRegistryScheme, UserLoginScheme
from app.multipart.models.user import User
from app.multipart.utils.auth import get_password_hash, create_access_token
from app.multipart.connection.cache import cache_redis
from app.env import REDIS_CACHE_EXP

async def create_new_user(user_data: UserRegistryScheme, session: AsyncSession) -> None:
    '''Создание нового пользователя в БД.'''
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(password=user_data.password)
    )
    session.add(new_user)


async def login_user(user_data: UserLoginScheme, session: AsyncSession) -> TokenScheme | None:
    '''Аутентификация пользователя'''
    user = await authenticate_user(session=session, user_login_form=user_data)  # Сверяем полученные логин и пароль с теми что в БД
    if user:
        token = create_access_token(
            data=TokenDataScheme(id_user=user.id),
        )
        await session.execute(update(User).where(User.id == user.id).values(token=token.token))  # В случае успеха создаем токен и кладем его в БД
        await cache_redis.set(
            name=str(user.id),
            value=token.token,
            ex=REDIS_CACHE_EXP
        )  # А так же в кэш
        await cache_redis.aclose()
        return token
    

async def logout_user(token: TokenScheme, session: AsyncSession) -> None:
    '''Разлогинивание пользователя'''
    user = await get_current_user(session=session, token=token)  # Получаем пользователя без проверки в черном списке
    if user:
        await session.execute(update(User).where(User.id == user.id).values(token=None))  # Удаляем токен из БД
        await session.commit()
        await cache_redis.delete(str(user.id))  # А так же из кэша
        await cache_redis.aclose()
