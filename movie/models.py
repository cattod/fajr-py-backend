from sqlalchemy import Column, String, ARRAY, Integer
from sqlalchemy.dialects.postgresql import UUID

from db_session import PrimaryModel, Base


class Movie(PrimaryModel,Base):
    __tablename__ = 'movies'

    title = Column(String, nullable=False)
    description = Column(String)
    director = Column(String)
    writer = Column(String)
    producer = Column(String)
    images = Column(ARRAY(UUID))
    genre = Column(ARRAY(String))
    pub_year = Column(String)
    order_filed = Column(Integer)


