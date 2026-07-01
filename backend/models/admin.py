# Placeholder for backend/models/admin.py
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database.database import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)

    username = Column(
        String,
        unique=True
    )

    password_hash = Column(String)