from sqlalchemy import String   , Boolean , DateTime
from sqlalchemy.orm   import Mapped , mapped_column
from datetime import datetime 
from .base import Base 

class User(Base): 

    __tablename__ = "users" 

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 


"""
Important Concepts:

Using SQLAlchemy 2.0 style with Mapped and mapped_column (type hints for ORM).

index=True on fields used in queries (email, id).

unique=True enforces uniqueness at DB level.

default=datetime.utcnow sets a default timestamp.

We'll add other models (Student, Teacher, Class) later.
"""