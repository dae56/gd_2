from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

import sys
sys.path.append('src')

from app.multipart.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    hashed_password: Mapped[str]
    token: Mapped[str | None] = mapped_column(default=None)
    disabled: Mapped[bool] = mapped_column(default=False)
    tasks = relationship('Task', back_populates='user')


    def __repr__(self) -> str:
        return f'|id: {self.id}, name: {self.name}|'
    