# Placeholder for backend/models/question.py
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from database.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    topic = Column(String)
    difficulty = Column(String)

    question = Column(Text)

    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)

    correct_answer = Column(String)