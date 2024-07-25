from pydantic import BaseModel


class TokenScheme(BaseModel):
    token: str


class TokenDataScheme(BaseModel):
    id_user: int
    