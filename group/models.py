from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_continuum import make_versioned

from db_session import Base, PrimaryModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint

from user.models import User

make_versioned(user_cls=None)

class Group(Base,PrimaryModel):
    __versioned__ = {}
    __tablename__ = 'groups'

    title = Column(String,unique=True,nullable=False)
    person_id = Column(UUID,ForeignKey('persons.id'))

class GroupUser(Base,PrimaryModel):
    __tablename__='group_users'

    group_id = Column(UUID,ForeignKey('groups.id'),nullable=False)
    user_id = Column(UUID,ForeignKey('users.id'),nullable=False)
    UniqueConstraint(group_id,user_id)

    group = relationship(Group, primaryjoin=group_id == Group.id)
    user = relationship(User,primaryjoin=user_id==User.id)


