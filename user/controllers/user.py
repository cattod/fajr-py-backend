import hashlib
import json
from bottle import response
from app_redis import app_redis as redis
from log import LogMsg, logger
from helper import model_to_dict, Http_error, edit_basic_data, \
    populate_basic_data
from messages import Message
from repository.person_repo import validate_person
from repository.user_repo import check_by_username, check_by_cell_no, \
    check_by_id, check_user
from user.models import User
from .person import get as get_person, add as add_person, edit as edit_person, \
    get_person_profile
from infrastructure.schema_validator import schema_validate
from ..constants import USER_ADD_SCHEMA_PATH, RESET_PASS_SCHEMA_PATH, \
    USER_EDIT_SCHEMA_PATH


def add(db_session, data, username):
    logger.info(LogMsg.START)
    schema_validate(data, USER_ADD_SCHEMA_PATH)
    logger.debug(LogMsg.SCHEMA_CHECKED)
    new_username = data.get('username')

    user = check_by_username(new_username, db_session)
    if user:
        logger.error(LogMsg.USER_XISTS, new_username)
        raise Http_error(409, Message.USERNAME_EXISTS)

    logger.debug(LogMsg.USR_ADDING)

    model_instance = User()
    model_instance.username = new_username
    model_instance.password = data.get('password')
    populate_basic_data(model_instance, username, data.get('tags'))
    logger.debug(LogMsg.POPULATING_BASIC_DATA)
    person_id = data.get('person_id')
    if person_id:
        person_is_valid = validate_person(person_id, db_session)
        logger.debug(LogMsg.PERSON_EXISTS, {'person_id': person_id})
        if person_is_valid:
            if person_is_valid.is_legal:
                person_user = get_by_person(person_id, db_session)
                if person_user is not None:
                    logger.error(LogMsg.LEGAL_PERSON_USER_RESTRICTION)
                    raise Http_error(409, Message.LEGAL_PERSON_USER_RESTRICTION)

            model_instance.person_id = person_id

        else:
            logger.error(LogMsg.INVALID_USER, {'person_id': person_id})
            raise Http_error(404, Message.INVALID_USER)

    db_session.add(model_instance)

    logger.debug(LogMsg.DB_ADD, model_to_dict(model_instance))
    logger.info(LogMsg.END)

    return model_instance


def get_by_person(person_id, db_session):
    return db_session.query(User).filter(User.person_id == person_id).first()


def get(id, db_session, username):
    logger.info(LogMsg.START, username)

    logger.debug(LogMsg.MODEL_GETTING, {'user_id': id})
    model_instance = db_session.query(User).filter(User.id == id).first()
    if model_instance:
        result = user_to_dict(model_instance)
        logger.debug(LogMsg.GET_SUCCESS, result)
    else:
        logger.debug(LogMsg.NOT_FOUND, {'user_id': id})
        raise Http_error(404, Message.NOT_FOUND)

    logger.info(LogMsg.END)

    return result


def get_profile(username, db_session):
    logger.info(LogMsg.START, username)

    logger.debug(LogMsg.MODEL_GETTING, {'user.username': username})
    model_instance = db_session.query(User).filter(
        User.username == username).first()

    if model_instance:
        profile = dict(get_person_profile(model_instance.person_id, db_session,
                                          username))

    else:
        logger.debug(LogMsg.NOT_FOUND, {'user.username': username})
        raise Http_error(404, Message.NOT_FOUND)

    result = model_to_dict(model_instance)
    result['person'] = profile

    del result['password']
    logger.debug(LogMsg.USER_PROFILE_IS, result)
    logger.info(LogMsg.END)

    return result


def delete(id, db_session, username):
    logger.info(LogMsg.START, username)
    user = db_session.query(User).filter(User.id == id).first()
    if user is None:
        logger.error(LogMsg.NOT_FOUND, {'user_id': id})
        raise Http_error(404, Message.NOT_FOUND)

    try:
        logger.debug(LogMsg.DELETE_REQUEST, {'user_id': id})
        logger.debug(LogMsg.GROUP_DELETE_USER_GROUPS, id)
        db_session.delete(user)

        logger.debug(LogMsg.DELETE_SUCCESS, {'user_id': id})

    except:
        logger.exception(LogMsg.DELETE_FAILED, exc_info=True)
        raise Http_error(500, LogMsg.DELETE_FAILED)
    logger.info(LogMsg.END)

    return {}


def get_all(db_session, username):
    logger.info(LogMsg.START, username)
    logger.debug(LogMsg.GET_ALL_REQUEST, "Users...")
    result = db_session.query(User).order_by(User.creation_date.desc()).all()

    final_res = []
    for item in result:
        final_res.append(user_to_dict(item))

    logger.debug(LogMsg.GET_SUCCESS, final_res)
    logger.info(LogMsg.END)

    return final_res


def serach_user(data, db_session, username):
    logger.info(LogMsg.START, username)

    if data.get('sort') is None:
        data['sort'] = ['creation_date-']

    result = User.mongoquery(
        db_session.query(User)).query(
        **data).end().all()
    final_res = []
    for item in result:
        final_res.append(user_to_dict(item))

    logger.debug(LogMsg.GET_SUCCESS, final_res)
    logger.info(LogMsg.END)

    return final_res


def edit(id, db_session, data, username):
    logger.info(LogMsg.START, username)
    schema_validate(data, USER_EDIT_SCHEMA_PATH)
    logger.debug(LogMsg.SCHEMA_CHECKED)

    old_pass = data.get('old_password', None)
    if old_pass is not None:
        user = check_user(username, db_session)
        if user.password != old_pass:
            logger.error(LogMsg.INVALID_USER, {'old_password': 'not correct'})
            raise Http_error(403, Message.INVALID_PASSWORD)

    logger.debug(LogMsg.EDIT_REQUST, {'user_id': id, 'data': data})

    model_instance = check_by_id(id, db_session)
    if model_instance:
        logger.debug(LogMsg.MODEL_GETTING, {'user_id': id})
    else:
        logger.debug(LogMsg.NOT_FOUND, {'user_id': id})
        raise Http_error(404, Message.NOT_FOUND)
    if model_instance.username == username:
        password = data.get('old_password')
        if model_instance.password != password:
            logger.error(LogMsg.INVALID_USER,
                         {'password': 'incorrect password'})
            raise Http_error(403, Message.INVALID_PASSWORD)
    for key, value in data.items():
        setattr(model_instance, key, value)
    edit_basic_data(model_instance, username, data.get('tags'))
    user_dict = user_to_dict(model_instance)

    logger.debug(LogMsg.EDIT_SUCCESS, user_dict)
    logger.info(LogMsg.END)

    return user_dict


def user_to_dict(user):
    if not isinstance(user, User):
        raise Http_error(400, LogMsg.NOT_RIGTH_ENTITY_PASSED.format('USER'))

    result = {
        'username': user.username,
        'creator': user.creator,
        'creation_date': user.creation_date,
        'id': user.id,
        'person_id': user.person_id,
        'person': model_to_dict(user.person),
        'version': user.version,
        'modification_date': user.modification_date,
        'modifier': user.modifier,
        'tags': user.tags
    }

    return result


def edit_profile(id, db_session, data, username):
    logger.info(LogMsg.START, username)

    logger.debug(LogMsg.EDIT_REQUST, data)

    user = get(id, db_session, username)
    if user:
        logger.debug(LogMsg.MODEL_GETTING, {'user_id': id})
        if user.person_id:
            person = get_person(user.person_id, db_session, username)
            logger.debug(LogMsg.PERSON_EXISTS, username)
            if person:
                edit_person(person.id, db_session, data, username)

            else:
                logger.error(LogMsg.USER_HAS_NO_PERSON, username)
                raise Http_error(404, LogMsg.PERSON_NOT_EXISTS)

        else:
            person = add_person(db_session, data, username)
            user.person_id = person.id

    else:
        logger.debug(LogMsg.NOT_FOUND, {'user_id': id})
        raise Http_error(404, Message.NOT_FOUND)

    user_dict = user_to_dict(user)
    logger.debug(LogMsg.MODEL_ALTERED, user_dict)

    logger.info(LogMsg.END)

    return user_dict


def reset_pass(data, db_session):
    logger.info(LogMsg.START, data)
    schema_validate(data, RESET_PASS_SCHEMA_PATH)
    logger.debug(LogMsg.SCHEMA_CHECKED)

    cell_no = data.get('cell_no')
    redis_key = 'PASS_{}'.format(cell_no)
    code = redis.get(redis_key)
    if code is None:
        logger.error(LogMsg.REGISTER_KEY_DOESNT_EXIST)
        raise Http_error(404, Message.INVALID_CODE)

    code = code.decode("utf-8")
    if (code is None) or (code != data.get('code')):
        logger.error(LogMsg.REGISTER_KEY_INVALID)
        raise Http_error(409, Message.INVALID_CODE)

    user = check_by_cell_no(cell_no, db_session)

    if user:
        user.password = data.get('password')

        logger.debug(LogMsg.USER_PASSWORD_RESET, user_to_dict(user))
        logger.info(LogMsg.END)

        return data

    logger.error(LogMsg.NOT_FOUND, data)
    raise Http_error(404, Message.INVALID_USER)


def head_profile(username, db_session):
    logger.info(LogMsg.START, username)
    profile = get_profile(username, db_session)
    profile_str = json.dumps(dict(profile)).encode()
    result_hash = hashlib.md5(profile_str).hexdigest()

    response.add_header('content_type', 'application/json')
    response.add_header('etag', result_hash)

    logger.info(LogMsg.END)
    return response
