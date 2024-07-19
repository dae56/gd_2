from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

import sys

sys.path.append('src')

from app.multipart.models.base import Base


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
