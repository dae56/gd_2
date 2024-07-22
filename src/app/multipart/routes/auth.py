from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request

import sys

sys.path.append('src')

from app.multipart.connection.database import get_async_session
from app.multipart.schemas import UserRegistryScheme, UserLoginScheme
from app.multipart import service
from app.env import COCKIE_MAX_AGE

router = APIRouter(
    tags=['auth']
)


@router.post('/register')
async def registry(user_data: UserRegistryScheme, session: AsyncSession = Depends(get_async_session)):
    res = await service.register(session=session, data=user_data)
    if res:
        await session.commit()
        return {'messege': f'User {user_data.name} is registered'}
    else:
        await session.rollback()
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Unknow eror',
        headers={"WWW-Authenticate": "JWT"}
    )


@router.post('/login')
async def login(responce: Response, user_data: UserLoginScheme, session: AsyncSession = Depends(get_async_session)):
    token = await service.login(session=session, data=user_data)
    if token:
        await session.commit()
        responce.set_cookie(
            key='jwt',
            value=token,
            max_age=COCKIE_MAX_AGE
        )
        return {'messege': 'User is authorize'}
    await session.rollback()
    raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Unknow eror',
    headers={"WWW-Authenticate": "JWT"}
)


@router.post('/logout')
async def logout(responce_req: Request, responce_jwt: Response, session: AsyncSession = Depends(get_async_session)):
    token = responce_req.cookies.get('jwt')
    if token:
        res = await service.logout(session=session, token=token)
        if res:
            await session.commit()
            responce_jwt.delete_cookie(key='jwt')
            return {'messege': 'User unauthorize'}
        await session.rollback()
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Unknow eror',
        headers={"WWW-Authenticate": "JWT"}
    )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid token',
        headers={"WWW-Authenticate": "JWT"}
    )