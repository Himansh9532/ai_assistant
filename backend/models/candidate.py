# Placeholder for backend/models/candidate.py
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from datetime import datetime

from database.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)

    college_company = Column(String)
    stream = Column(String)
    experience = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )