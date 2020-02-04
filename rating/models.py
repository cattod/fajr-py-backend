from sqlalchemy import Column, String, ForeignKey, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_continuum import make_versioned

from db_session import PrimaryModel, Base
from movie.models import Movie
from user.models import Person

make_versioned(user_cls=None)

class Rating(PrimaryModel,Base):
    __versioned__ = {}
    __tablename__ = 'ratings'

    movie_id = Column(UUID,ForeignKey(Movie.id),nullable=False)
    person_id = Column(UUID,ForeignKey(Person.id),nullable=False)
    overall_rate = Column(Float)
    comment = Column(String)
    novel = Column(Float)
    character = Column(Float)
    reason = Column(Float)
    directing = Column(Float)
    acting = Column(Float)
    editing = Column(Float)
    visualization = Column(Float)
    sound = Column(Float)
    music = Column(Float)
    violence_range = Column(Float)
    insulting_range = Column(Float)
    sexual_content = Column(Float)
    unsuitable_wearing = Column(Float)
    addiction_promotion = Column(Float)
    horror_content = Column(Float)
    suicide_encouragement = Column(Float)
    breaking_law_encouragement = Column(Float)
    gambling_promotion = Column(Float)
    alcoholic_promotion = Column(Float)
    family_subject = Column(Float)
    individual_social_behavior = Column(Float)
    feminism_exposure = Column(Float)
    justice_seeking = Column(Float)
    theism = Column(Float)
    bright_future_exposure = Column(Float)
    hope = Column(Float)
    iranian_life_style = Column(Float)
    true_vision_of_enemy = Column(Float)
    true_historiography = Column(Float)
    question_1 = Column(String)
    question_2 = Column(String)
    question_3 = Column(String)
    question_4 = Column(String)
    question_5 = Column(String)
    question_6 = Column(String)
    question_7 = Column(String)
    question_8 = Column(String)
    question_9 = Column(String)
    question_10 = Column(String)

    movie = relationship(Movie, primaryjoin=movie_id == Movie.id , lazy=True)
    person = relationship(Person, primaryjoin=person_id == Person.id , lazy=True)
