from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

import sys
sys.path.append('src')

from app.multipart.models.base import Base


class Task(Base):  # Модель таблицы задач
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='tasks', uselist=False)


    def __repr__(self) -> str:
        return f'|id: {self.id}, text: {self.text}|'
    