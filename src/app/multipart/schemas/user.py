from pydantic import BaseModel, EmailStr, Field


class UserLoginScheme(BaseModel):
    email: EmailStr
    password: str = Field(max_length=30)


class UserRegistryScheme(UserLoginScheme):
    name: str = Field(max_length=50)


class UserScheme(BaseModel):
    id: int
    name: str = Field(max_length=50)
    email: EmailStr
    hashed_password: str
    token: str | None
    disabled: bool
    