from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request

import sys

sys.path.append('src')

from app.multipart.connection.database import get_async_session
from app.multipart.schemas.user import UserRegistryScheme, UserLoginScheme
from app.multipart.schemas.token import TokenScheme
from app.multipart.crud.auth import create_new_user, login_user, logout_user
from app.env import COCKIE_MAX_AGE

router = APIRouter(
    tags=['auth']
)


@router.post('/register')
async def register(user_data: UserRegistryScheme, session: AsyncSession = Depends(get_async_session)) -> dict[str, str]:
    '''Регистрация новых пользователей.'''
    await create_new_user(user_data=user_data, session=session)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User alredy exist!'
        )
    return {'message': f'user {user_data.name} is registered!'}


@router.post('/login')
async def login(responce: Response, request: Request, user_data: UserLoginScheme, session: AsyncSession = Depends(get_async_session)) -> dict[str, str]:
    '''Логинирование пользователей.'''
    if request.cookies.get('auth'):  # Если куки для токена есть то не пускаем дальше
        return {'message': 'The user is already authenticated!'}
    token = await login_user(user_data=user_data, session=session)
    if not token:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User does not exist!'
        )
    await session.commit()
    responce.set_cookie(  # Устанавливаем токен в куки
        key='auth',
        value=token.token,
        max_age=COCKIE_MAX_AGE,
        secure=True,
        httponly=True
    )
    return {'message': 'Authentication was successful!'}


@router.post('/logout')
async def logout(responce: Response, request: Request, session: AsyncSession = Depends(get_async_session)) -> dict[str, str]:
    '''Разлогинивание пользователей.'''
    token = request.cookies.get('auth')
    if token:
        responce.delete_cookie(key='auth')
        await logout_user(token=TokenScheme(token=token), session=session)
    return {'message': 'User unauthentication!'}