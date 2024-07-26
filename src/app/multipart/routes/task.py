from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query

import sys

sys.path.append('src')

from app.multipart.connection.database import get_async_session
from app.multipart.schemas.task import CreateTaskScheme
from app.multipart.schemas.token import TokenScheme
from app.multipart.crud.task import create_task, get_tasks, get_task, update_task, del_task


router = APIRouter(
    tags=['tasks'],
    prefix='/tasks'
)

unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='User unauthenticate!'
    )


@router.post('/')
async def create_new_task(responce: Request, new_task: CreateTaskScheme, session: AsyncSession = Depends(get_async_session)):
    '''Создание новой записи.'''
    token = responce.cookies.get('auth')
    if token:
        res = await create_task(session=session, new_task=new_task, token=TokenScheme(token=token))
        if res:
            return {'message': 'Task created!'}
    raise unauth_exc


@router.get('/')
async def get_all_tasks(
    responce: Request,
    offset: int = Query(default=0, ge=0),
    count: int = Query(default=1, ge=0, le=100),
    session: AsyncSession = Depends(get_async_session)):
    '''Получение всех записей (применена пагинация).'''
    token = responce.cookies.get('auth')
    if token:
        tasks = await get_tasks(session=session, token=TokenScheme(token=token), offset=offset, count=count)
        if tasks:
            return {'User tasks': tasks}
        return {'message': 'The user has no tasks'}
    raise unauth_exc


@router.get('/{task_id}')
async def get_cur_task(responce: Request, task_id: int, session: AsyncSession = Depends(get_async_session)):
    '''Получение конкретной задачи.'''
    token = responce.cookies.get('auth')
    if token:
        task = await get_task(session=session, token=TokenScheme(token=token), task_id=task_id)
        if task:
            return task
        return {'message': 'The user does not have such a task'}
    raise unauth_exc


@router.put('/{task_id}')
async def update_cur_task(
    responce: Request,
    task_id: int,
    task_data: CreateTaskScheme,
    session: AsyncSession = Depends(get_async_session)):
    '''Обновление конкретной записи.'''
    token = responce.cookies.get('auth')
    if token:
        task = await update_task(session=session, token=TokenScheme(token=token), task_id=task_id, new_task_data=task_data)
        if task:
            return {'message': 'Task updated!',
                    'new data task': task
                    }
        return {'message': 'The user does not have such a task'}
    raise unauth_exc


@router.delete('/{task_id}')
async def delete_cur_task(responce: Request, task_id: int, session: AsyncSession = Depends(get_async_session)):
    '''Удаление конкретной записи.'''
    token = responce.cookies.get('auth')
    if token:
        res = await del_task(session=session, token=TokenScheme(token=token), task_id=task_id)
        if res == True:
            return {'message': 'Task deleted!'}
        elif res == False:
            return {'message': 'The user does not have such a task'}
    raise unauth_exc
