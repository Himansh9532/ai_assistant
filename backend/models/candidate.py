from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from database.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)

    college_company = Column(String, nullable=True, default="")
    stream = Column(String, nullable=True, default="")
    experience = Column(String, nullable=True, default="")
    password_hash = Column(String, nullable=True)
    is_verified = Column(Integer, default=0)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )