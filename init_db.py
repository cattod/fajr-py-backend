from uuid import uuid4

from db_migration.permissions import permissions_to_db
from permission.controllers.group_permission import premium_permission_group
from user.models import Person, User
from group.models import Group, GroupUser
from db_session import db_session
from helper import Now


def init_db():
    person = Person()
    person.id = str(uuid4())
    person.version = 1
    person.creation_date = Now()
    person.creator = 'DB_INIT'
    person.name = 'Admin'
    person.last_name = 'Admin'
    person.cell_no = '11111111111'
    db_session.add(person)
    db_session.flush()

    print('person added by data : {name:{},last_name:{},id:{}'.format(person.name,
                                                                      person.last_name,
                                                                      person.id))

    user = User()
    user.id = str(uuid4())
    user.version = 1
    user.creation_date = Now()
    user.creator = 'DB_INIT'
    user.username = 'admin'
    user.password = 'Admin@filmsanj#1398_Lol'
    user.person_id = person.id

    db_session.add(user)
    db_session.flush()

    print('user added by data : {username:{},password:{},id:{}'.format(user.username,
                                                                      user.password,
                                                                      user.id))

    group = Group()
    group.id = str(uuid4())
    group.version = 1
    group.creation_date = Now()
    group.creator = 'DB_INIT'
    group.title = 'Administrators'
    group.person_id = person.id

    db_session.add(group)
    db_session.flush()

    print('group added by data : {title:{},person_id:{},id:{}'.format(group.title,
                                                                       group.person_id,
                                                                       group.id))

    gu = GroupUser()
    gu.id = str(uuid4())
    gu.version = 1
    gu.creation_date = Now()
    gu.creator = 'DB_INIT'
    gu.group_id = group.id
    gu.user_id = user.id

    db_session.add(gu)
    print('user_group added by data : {group_id:{},user_id:{},id:{}'.format(gu.group_id,
                                                                      gu.user_id,
                                                                      gu.id))

    permissions = permissions_to_db(db_session, user.username)
    db_session.flush()
    print('permissions added to DB : {}'.format(permissions))

    premium_permission_group(group.id, db_session, user.username)

    db_session.commit()
    print('premium permissions added to group : {}'.format(group.id))


    return {'result': 'successful'}


if __name__ == '__main__':
    result = init_db()
    print(result)
