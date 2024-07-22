from fastapi import HTTPException, status

from datetime import datetime, timedelta, timezone
import hashlib
import jwt

import sys
sys.path.append('src')

from app.env import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, PASS_SALT


def get_password_hash(password: str) -> str:
    pwd = password + PASS_SALT
    return hashlib.md5(pwd.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd = plain_password + PASS_SALT
    if hashlib.md5(pwd.encode()).hexdigest() == hashed_password:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "JWT"}
    )


def create_access_token(id_user: int) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        payload={
            'sub': id_user,
            'exp': exp
        },
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_acces_token(token: str) -> dict[str, int]:
    try:
        payload = jwt.decode(
        jwt=token,
        key=SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid token',
        headers={"WWW-Authenticate": "JWT"}
    )
    else:
        return payload
