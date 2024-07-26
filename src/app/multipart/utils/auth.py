import hashlib
from datetime import datetime, timedelta, timezone
import jwt

import sys
sys.path.append('src')

from app.env import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, PASS_SALT
from app.multipart.schemas.token import TokenDataScheme, TokenScheme


def verify_password(plain_password: str, hashed_password: str) -> bool:  # Проверка на совпадение паролей
    db_pass = plain_password + PASS_SALT
    hashed = hashlib.md5(db_pass.encode())
    return hashed.hexdigest() == hashed_password


def get_password_hash(password: str) -> str:  # Получение хеша пароля
    db_pass = password + PASS_SALT
    hashed = hashlib.md5(db_pass.encode())
    return hashed.hexdigest()


def create_access_token(data: TokenDataScheme) -> TokenScheme:  # Генерация токена
    to_encode = data.id_user
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return TokenScheme(token=jwt.encode(payload={
        'sub': to_encode,
        'exp': expire
    }, key=SECRET_KEY, algorithm=ALGORITHM))


def decode_acces_token(token: TokenScheme) -> TokenDataScheme | None:  # Дешифровка токена
    try:
        payload = jwt.decode(jwt=token.token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    return TokenDataScheme(id_user=payload['sub'])