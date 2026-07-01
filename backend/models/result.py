from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import String

from database.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id")
    )

    score = Column(Integer)

    percentage = Column(Float)

    grade = Column(String(10))

    feedback = Column(Text)