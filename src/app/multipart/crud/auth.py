from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

import sys

sys.path.append('src')

from app.multipart.crud.service import authenticate_user, get_current_user
from app.multipart.schemas.token import TokenDataScheme, TokenScheme
from app.multipart.schemas.user import UserRegistryScheme, UserLoginScheme
from app.multipart.models.user import User
from app.multipart.utils.auth import get_password_hash, create_access_token


async def create_new_user(user_data: UserRegistryScheme, session: AsyncSession) -> None:
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(password=user_data.password)
    )
    session.add(new_user)


async def login_user(user_data: UserLoginScheme, session: AsyncSession) -> TokenScheme | None:
    user = await authenticate_user(session=session, user_login_form=user_data)
    if user:
        token = create_access_token(
            data=TokenDataScheme(id_user=user.id),
        )
        await session.execute(update(User).where(User.id == user.id).values(token=token.token))
        return token
    

async def logout_user(token: TokenScheme, session: AsyncSession) -> None:
    user = await get_current_user(session=session, token=token)
    if user:
        await session.execute(update(User).where(User.id == user.id).values(token=None))
        await session.commit()
