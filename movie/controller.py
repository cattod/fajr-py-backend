from check_permission import validate_permissions_and_access
from infrastructure.schema_validator import schema_validate
from log import logger, LogMsg
from helper import populate_basic_data, model_to_dict, Http_error, edit_basic_data, \
    Http_response
from messages import Message
from movie.constants import MOVIE_ADD_SCHEMA_PATH, MOVIE_EDIT_SCHEMA_PATH
from movie.models import Movie
from repository.rating_repo import users_rated_movie_ids


def add(data,db_session,username):
    logger.info(LogMsg.START, username)
    schema_validate(data, MOVIE_ADD_SCHEMA_PATH)
    logger.debug(LogMsg.SCHEMA_CHECKED)

    logger.debug(LogMsg.PERMISSION_CHECK, username)
    validate_permissions_and_access(username, db_session, 'ADD_MOVIE')
    logger.debug(LogMsg.PERMISSION_VERIFIED)

    model_instance = Movie()
    populate_basic_data(model_instance,username,data.get('tags'))
    logger.debug(LogMsg.POPULATING_BASIC_DATA)
    model_instance.description = data.get('description')
    model_instance.title = data.get('title')
    model_instance.images = data.get('images')
    model_instance.director = data.get('director')
    model_instance.producer = data.get('producer')
    model_instance.pub_year = data.get('pub_year')
    model_instance.genre = data.get('genre')
    model_instance.writer = data.get('writer')

    db_session.add(model_instance)
    logger.debug(LogMsg.DB_ADD)
    logger.info(LogMsg.END,model_to_dict(model_instance))
    return model_instance

def get(id,db_session,username):
    logger.info(LogMsg.START,username)

    logger.debug(LogMsg.PERMISSION_CHECK, username)
    validate_permissions_and_access(username, db_session, 'GET_MOVIE')
    logger.debug(LogMsg.PERMISSION_VERIFIED)

    result =db_session.query(Movie).filter(Movie.id==id).first()
    final_res = model_to_dict(result)
    logger.debug(LogMsg.GET_SUCCESS,final_res)
    logger.info(LogMsg.END)
    return final_res

def get_all(data, db_session, username):
    logger.info(LogMsg.START, username)

    if data.get('sort') is None:
        data['sort'] = ['creation_date-']

    result = Movie.mongoquery(
        db_session.query(Movie)).query(
        **data).end().all()
    final_res = []
    rated_movies = users_rated_movie_ids(username, db_session)
    for item in result:
        model_dict = model_to_dict(item)
        model_dict['rated_by_user'] = False
        if item.id in rated_movies:
            model_dict['rated_by_user'] = True
        final_res.append(model_dict)

    logger.debug(LogMsg.GET_SUCCESS, final_res)
    logger.info(LogMsg.END)

    return final_res

def edit(id,data,db_session,username):
    logger.info(LogMsg.START, username)
    schema_validate(data, MOVIE_EDIT_SCHEMA_PATH)
    logger.debug(LogMsg.SCHEMA_CHECKED)


    logger.debug(LogMsg.PERMISSION_CHECK, username)
    validate_permissions_and_access(username, db_session, 'EDIT_MOVIE')
    logger.debug(LogMsg.PERMISSION_VERIFIED)

    model_instance = db_session.query(Movie).filter(Movie.id==id).first()
    if model_instance is None:
        logger.error(LogMsg.NOT_FOUND,{'movie_id':id})
        raise Http_error(404,Message.NOT_FOUND)
    try:
        for key, value in data.items():
            # TODO  if key is valid attribute of class
            setattr(model_instance, key, value)
        edit_basic_data(model_instance, username, data.get('tags'))
        logger.debug(LogMsg.EDIT_SUCCESS,model_to_dict(model_instance))
    except:
        logger.exception(LogMsg.EDIT_FAILED,exc_info=True)
        raise Http_error(409,Message.EDIT_FAILED)
    logger.info(LogMsg.END)
    return model_to_dict(model_instance)

def delete(id,db_session,username):
    logger.info(LogMsg.START,username)

    logger.debug(LogMsg.PERMISSION_CHECK, username)
    validate_permissions_and_access(username, db_session, 'DELETE_MOVIE')
    logger.debug(LogMsg.PERMISSION_VERIFIED)

    model_instance = db_session.query(Movie).filter(Movie.id==id).first()
    if model_instance is None:
        logger.error(LogMsg.NOT_FOUND, {'movie_id': id})
        raise Http_error(404, Message.NOT_FOUND)
    try:
        db_session.delete(model_instance)
        logger.debug(LogMsg.DELETE_SUCCESS,{'movie_id':id})
    except:
        logger.exception(LogMsg.DELETE_FAILED,exc_info=True)
        raise Http_error(409,Message.DELETE_FAILED)
    logger.info(LogMsg.END)
    return Http_response(204,True)
