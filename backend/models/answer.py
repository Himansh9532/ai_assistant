# Placeholder for backend/models/answer.py
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from database.database import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id")
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id")
    )

    selected_answer = Column(String)