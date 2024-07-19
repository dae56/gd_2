from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

import sys

sys.path.append('src')

from app.multipart.models.base import Base


class User(Base):
    __tablename__ =  'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str]
