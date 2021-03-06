from helper import Http_error
from messages import Message
from user.models import User, Person


def check_user(username, db_session):
    return db_session.query(User).filter(User.username == username).first()

def check_by_cell_no(cell_no,db_session):
    user = db_session.query(User).filter(User.username == cell_no).first()
    if not user:
        person = db_session.query(Person).filter(Person.cell_no == cell_no).first()
        if person is not None:
            user = db_session.query(User).filter(User.person_id == person.id).first()

    return user


def check_by_username(username,db_session):
    user = db_session.query(User).filter(User.username == username).first()

    return user


def check_by_id(id,db_session):
    user = db_session.query(User).filter(User.id == id).first()

    return user


def validate_users(user_list, db_session):
    result = db_session.query(User).filter(
        User.id.in_(set(user_list))).all()
    if (result is not None) and (len(set(user_list)) == len(result)):
        return result
    else:
        raise Http_error(404, Message.INVALID_USER)

def user_count(db_session):
    return db_session.query(User).count()


def persons_by_user(user_list,db_session):
    result = db_session.query(User).filter(User.id.in_(user_list)).all()
    final_res = []
    for user in result:
        final_res.append(user.person_id)
    return final_res
