from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request

import sys

sys.path.append('src')

from app.multipart.connection.database import get_async_session
from app.multipart.schemas import UserRegistryScheme, UserLoginScheme
from app.multipart import service
from app.multipart.models import Task


router = APIRouter(
    tags=['tasks'],
    prefix='/tasks'
)


@router.post('/')
async def create_task(responce: Request, text_task: str, session: AsyncSession = Depends(get_async_session)):
    token = responce.cookies.get('jwt')
    if token:
        res = await service.create_new_task(session=session, token=token, text_task=text_task)
        if res:
            await session.commit()
            return {'messege': 'task created!'}
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Unknow error',
        headers={"WWW-Authenticate": "JWT"}
    )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid token',
        headers={"WWW-Authenticate": "JWT"}
    )


@router.get('/')
async def get_all_tasks(responce: Request, session: AsyncSession = Depends(get_async_session)):
    token = responce.cookies.get('jwt')
    if token:
        tasks = await service.get_all_task(session=session, token=token)
        return {
            'tasks user': tasks
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Unknow error',
        headers={"WWW-Authenticate": "JWT"}
    )


@router.get('/{task_id}')
async def get_cur_task(responce: Request, task_id: int, session: AsyncSession = Depends(get_async_session)):
    token = responce.cookies.get('jwt')
    if token:
        tasks: list[Task] = await service.get_all_task(session=session, token=token)
        cur_task = list(filter(lambda x: x if x.id == task_id else False, tasks))
        return {
            'current task': cur_task[0]
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Unknow error',
        headers={"WWW-Authenticate": "JWT"}
    )


@router.put('/{task_id}')
async def update_cur_task(responce: Request, task_id: int, new_text: str, session: AsyncSession = Depends(get_async_session)):
    token = responce.cookies.get('jwt')
    if token:
        res = await service.update_task(session=session, token=token, task_id=task_id, new_text=new_text)
        if res:
            await session.commit()
            return {'messege': 'task upgraded'}
    await session.roolback()
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Unknow error',
        headers={"WWW-Authenticate": "JWT"}
    )


@router.delete('/{task_id}')
async def delete_cur_task(responce: Request, task_id: int, session: AsyncSession = Depends(get_async_session)):
    token = responce.cookies.get('jwt')
    if token:
        res = await service.delete_task(session=session, token=token, task_id=task_id)
        if res:
            await session.commit()
            return {'messege': 'task deleted'}
    await session.rollback()
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Unknow error',
        headers={"WWW-Authenticate": "JWT"}
    )