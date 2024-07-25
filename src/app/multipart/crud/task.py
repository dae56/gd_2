from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_

import sys

sys.path.append('src')

from app.multipart.crud.service import get_current_active_user
from app.multipart.schemas.task import CreateTaskScheme, TaskScheme
from app.multipart.schemas.token import TokenScheme
from app.multipart.models.task import Task


async def create_task(session: AsyncSession, new_task: CreateTaskScheme, token: TokenScheme) -> bool | None:
    user = await get_current_active_user(session=session, token=token)
    if user:
        task = Task(
            name=new_task.name,
            text=new_task.text,
            user_id=user.id
        )
        session.add(task)
        await session.commit()
        return True


async def get_tasks(session: AsyncSession, token: TokenScheme, offset: int, count: int) -> list[TaskScheme] | None:
    user = await get_current_active_user(session=session, token=token)
    if user:
        res = await session.execute(select(Task).where(Task.user == user).limit(count).offset(offset))
        tasks = res.scalars().all()
        if tasks:
            return [
                TaskScheme(
                    id=task.id,
                    name=task.name,
                    text=task.text,
                    user_id=task.user_id
                ) for task in tasks
            ]
        

async def get_task(session: AsyncSession, token: TokenScheme, task_id: int) -> TaskScheme | None:
    user = await get_current_active_user(session=session, token=token)
    if user:
        res = await session.execute(select(Task).where(and_(Task.user == user, Task.id == task_id)))
        task = res.scalar()
        if task:
            return TaskScheme(
                id=task.id,
                name=task.name,
                text=task.text,
                user_id=task.user_id
            )
        

async def update_task(session: AsyncSession, token: TokenScheme, task_id: int, new_task_data: CreateTaskScheme) -> TaskScheme | None:
    user = await get_current_active_user(session=session, token=token)
    if user:
        await session.execute(update(Task).where(and_(Task.user == user, Task.id == task_id)).values(
            name=new_task_data.name, text=new_task_data.text))
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
        else:
            res = await session.execute(select(Task).where(and_(Task.user == user, Task.id == task_id)))
            task = res.scalar()
            if task:
                return TaskScheme(
                    id=task.id,
                    name=task.name,
                    text=task.text,
                    user_id=task.user_id
                )
            

async def del_task(session: AsyncSession, token: TokenScheme, task_id: int) -> bool | None:
    user = await get_current_active_user(session=session, token=token)
    if user:
        res = await session.execute(select(Task).where(and_(Task.user == user, Task.id == task_id)))
        task = res.scalar()
        if task:
            await session.execute(delete(Task).where(and_(Task.user == user, Task.id == task_id)))
            await session.commit()
            return True
        return False
    