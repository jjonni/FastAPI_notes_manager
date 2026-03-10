import re

from datetime import datetime
from typing import List
from sqlalchemy import String, DateTime, func, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates

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

    @validates("email")
    def validate_email(self, key, value):
        if not re.match(r'[^@\s]+@[^@\s]+\.[^@\s]+', value):
            raise ValueError(f"{key} must be a valid email")
        return value

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

