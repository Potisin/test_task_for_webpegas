from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30))

