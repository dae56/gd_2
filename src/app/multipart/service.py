from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete, update, and_

import sys

sys.path.append('src')

from app.multipart.schemas import UserRegistryScheme, UserLoginScheme, UserScheme
from app.multipart.models import User, Task
from app.multipart.utils.auth import get_password_hash, verify_password
from app.multipart.utils.auth import create_access_token, decode_acces_token


async def get_user(session: AsyncSession, user_email: str) -> UserScheme | None:
    res = await session.execute(select(User).where(User.email == user_email))
    user_list = res.scalars().all()
    if user_list:
        return user_list[0]
    return None


async def get_current_user(session: AsyncSession, user_id: int, select_in_load = None) -> User | None:
    if select_in_load:
        res = await session.execute(select(User).where(User.id == user_id).options(selectinload(select_in_load)))
    else:
        res = await session.execute(select(User).where(User.id == user_id))
    user_list = res.scalars().all()
    if user_list:
        return user_list[0]
    return None
    

async def auth_user(session: AsyncSession, data: UserLoginScheme) -> User | None:
    user = await get_user(session=session, user_email=data.email)
    if user:
        if verify_password(
            plain_password=data.password,
            hashed_password=user.hashed_password
        ):
            return user
    return None


async def register(session: AsyncSession, data: UserRegistryScheme) -> bool:
    res = await get_user(session=session, user_email=data.email)
    if not res:
        new_user = User(
            name=data.name,
            email=data.email,
            hashed_password=get_password_hash(data.password)
        )
        session.add(new_user)
        return True
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='User already exists',
        headers={"WWW-Authenticate": "JWT"}
    )


async def login(session: AsyncSession, data: UserRegistryScheme) -> str:
    user = await auth_user(session=session, data=data)
    if user:
        token = create_access_token(user.id)
        await session.execute(update(User).where(User.id == user.id).values(token=token))
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "JWT"}
    )


async def logout(session: AsyncSession, token: str) -> bool:
    user_id = decode_acces_token(token=token)['sub']
    user = await get_current_user(session=session, user_id=user_id)
    if user:
        await session.execute(update(User).where(User.id == user.id).values(token=None))
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "JWT"}
    )


async def create_new_task(session: AsyncSession, token: str, text_task: str):
    user_id = decode_acces_token(token=token)['sub']
    user = await get_current_user(session=session, user_id=user_id)
    if user:
        new_task = Task(
            text=text_task,
            user_id=user.id
        )
        session.add(new_task)
        return True
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Unknow eror',
        headers={"WWW-Authenticate": "JWT"}
    )


async def get_all_task(session: AsyncSession, token: str):
    user_id = decode_acces_token(token=token)['sub']
    user = await get_current_user(session=session, user_id=user_id, select_in_load=User.tasks)
    if user:
        return user.tasks
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Unknow eror',
        headers={"WWW-Authenticate": "JWT"}
    )


async def update_task(session: AsyncSession, token: str, task_id: int, new_text: str):
    user_id = decode_acces_token(token=token)['sub']
    await session.execute(update(Task).where(and_(Task.id == task_id, Task.user_id == user_id)).values(text=new_text))
    res = await session.execute(select(Task).where(and_(Task.id == task_id, Task.user_id == user_id)))
    tasks = res.scalars().all()
    if tasks:
        if tasks[0].text == new_text:
            return True
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Unknow error',
        headers={"WWW-Authenticate": "JWT"}
    )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Task does not exist',
        headers={"WWW-Authenticate": "JWT"}
    )


async def delete_task(session: AsyncSession, token: str, task_id: int):
    user_id = decode_acces_token(token=token)['sub']
    await session.execute(delete(Task).where(and_(Task.id == task_id, Task.user_id == user_id)))
    return True
