from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import sys

sys.path.append('src')

from app.multipart.schemas.token import TokenScheme
from app.multipart.schemas.user import UserLoginScheme
from app.multipart.models.user import User
from app.multipart.utils.auth import verify_password, decode_acces_token


async def get_user(session: AsyncSession, id_user: int) -> User | None:
    result = await session.execute(select(User).where(User.id == id_user))
    user = result.scalar()
    if user:
        return user


async def authenticate_user(session: AsyncSession, user_login_form: UserLoginScheme) -> User | None:
    result = await session.execute(select(User).where(User.email == user_login_form.email))
    user = result.scalar()
    if user:
       if verify_password(user_login_form.password, user.hashed_password):
           return user


async def get_current_user(session: AsyncSession, token: TokenScheme) -> User | None:
    result = await session.execute(select(User).where(User.token == token.token))
    user = result.scalar()
    token_data = decode_acces_token(token=token)
    if token_data and user:
        user_id = token_data.id_user
        if user_id == user.id:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )


async def get_current_active_user(session: AsyncSession, token: TokenScheme) -> User | None:
    user = await get_current_user(session=session, token=token)
    if user:
        if user.disabled:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied",
        )
        return user
    