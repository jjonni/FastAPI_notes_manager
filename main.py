import logging

from datetime import datetime
from typing import List
from config.config import load_config, Config

from sqlalchemy import URL, create_engine, String, DateTime, func, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

config: Config = load_config()

logging.basicConfig(
    level=config.log.level,
    format=config.log.format
)

url_object = URL.create(
    drivername="postgresql+psycopg",
    username=config.db.user,
    password=config.db.password,
    host=config.db.host,
    database=config.db.name,
    port=config.db.port
)

# Пока что для закрепления материала, прочитанного в туториале из документации SQLAlchemy, будет использоваться синхронный интерфейс
engine = create_engine(url_object)

class Base(DeclarativeBase):
    pass

# SQLModel будет добавлен позже
# На данный момент цель — усвоить и по-возможности запомнить, как задаются ORM классы

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)  # Нужно добавить валидацию данных
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    notes: Mapped[List["Note"]] = relationship(back_populates="user")

class Note(Base):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    title: Mapped[String]
    content: Mapped[String]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user: Mapped[User] = relationship(back_populates="notes")
    note_tags: Mapped[List["NoteTag"]] = relationship(back_populates="notes")

class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag_name: Mapped[str] = mapped_column(String(20), unique=True)

    note_tags: Mapped[List["NoteTag"]] = relationship(back_populates="tag")

class NoteTag(Base):
    __tablename__ = "note_tag"

    note_id: Mapped[int] = mapped_column(ForeignKey("note.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"))

    __table_args__ = (
        PrimaryKeyConstraint("note_id", "tag_id")
    )

    note: Mapped[Note] = relationship(back_populates="note_tags")
    tag: Mapped[Tag] = relationship(back_populates="note_tags")