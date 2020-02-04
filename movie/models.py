from sqlalchemy import Column, String, ARRAY, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_continuum import make_versioned

from db_session import PrimaryModel, Base

make_versioned(user_cls=None)

class Movie(PrimaryModel,Base):
    __versioned__ = {}
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


