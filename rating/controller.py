from infrastructure.schema_validator import schema_validate
from log import logger, LogMsg
from helper import populate_basic_data, model_to_dict, Http_error, edit_basic_data, \
    Http_response, model_basic_dict
from messages import Message
from user.controllers.person import person_to_dict
from .constants import RATING_ADD_SCHEMA_PATH, RATING_EDIT_SCHEMA_PATH
from .models import Rating


def add(data, db_session, username):
    logger.info(LogMsg.START, username)
    # schema_validate(data, RATING_ADD_SCHEMA_PATH)
    # logger.debug(LogMsg.SCHEMA_CHECKED)
    rated = internal_get(data.get('person_id'), data.get('movie_id'), db_session)
    if rated is not None:
        result =  edit(rated.id, data, db_session, username)
        return result
    model_instance = Rating()
    populate_basic_data(model_instance, username, data.get('tags'))
    logger.debug(LogMsg.POPULATING_BASIC_DATA)

    model_instance.movie_id = data.get('movie_id')
    model_instance.person_id = data.get('person_id')
    model_instance.comment = data.get('comment')
    model_instance.overall_rate = data.get('overall_rate')
    model_instance.novel = data.get('novel')
    model_instance.character = data.get('character')
    model_instance.reason = data.get('reason')
    model_instance.directing = data.get('directing')
    model_instance.true_vision_of_enemy = data.get('true_vision_of_enemy')
    model_instance.iranian_life_style = data.get('iranian_life_style')
    model_instance.hope = data.get('hope')
    model_instance.bright_future_exposure = data.get('bright_future_exposure')
    model_instance.theism = data.get('theism')
    model_instance.justice_seeking = data.get('justice_seeking')
    model_instance.feminism_exposure = data.get('feminism_exposure')
    model_instance.individual_social_behavior = data.get('individual_social_behavior')
    model_instance.family_subject = data.get('family_subject')
    model_instance.alcoholic_promotion = data.get('alcoholic_promotion')
    model_instance.gambling_promotion = data.get('gambling_promotion')
    model_instance.breaking_law_encouragement = data.get('breaking_law_encouragement')
    model_instance.suicide_encouragement = data.get('suicide_encouragement')
    model_instance.horror_content = data.get('horror_content')
    model_instance.addiction_promotion = data.get('addiction_promotion')
    model_instance.unsuitable_wearing = data.get('unsuitable_wearing')
    model_instance.sexual_content = data.get('sexual_content')
    model_instance.insulting_range = data.get('insulting_range')
    model_instance.violence_range = data.get('violence_range')
    model_instance.music = data.get('music')
    model_instance.sound = data.get('sound')
    model_instance.visualization = data.get('visualization')
    model_instance.editing = data.get('editing')
    model_instance.acting = data.get('acting')
    model_instance.true_historiography = data.get('true_historiography')
    model_instance.question_1 = data.get('question_1')
    model_instance.question_2 = data.get('question_2')
    model_instance.question_3 = data.get('question_3')
    model_instance.question_4 = data.get('question_4')
    model_instance.question_5 = data.get('question_5')
    model_instance.question_6 = data.get('question_6')
    model_instance.question_7 = data.get('question_7')
    model_instance.question_8 = data.get('question_8')
    model_instance.question_9 = data.get('question_9')
    model_instance.question_10 = data.get('question_10')

    db_session.add(model_instance)
    logger.debug(LogMsg.DB_ADD)
    return model_instance


def get(id, db_session, username):
    logger.info(LogMsg.START, username)
    result = db_session.query(Rating).filter(Rating.id == id).first()
    final_res = rating_to_dict(result)
    logger.debug(LogMsg.GET_SUCCESS, final_res)
    logger.info(LogMsg.END)
    return final_res


def internal_get(person_id, movie_id, db_session):
    return  db_session.query(Rating).filter(Rating.person_id == person_id,
                                           Rating.movie_id == movie_id).first()


def get_all(data, db_session, username):
    logger.info(LogMsg.START, username)

    if data.get('sort') is None:
        data['sort'] = ['creation_date-']

    result = Rating.mongoquery(
        db_session.query(Rating)).query(
        **data).end().all()
    final_res = []
    for item in result:
        final_res.append(rating_to_dict(item))

    logger.debug(LogMsg.GET_SUCCESS, final_res)
    logger.info(LogMsg.END)

    return final_res


def edit(id, data, db_session, username):
    logger.info(LogMsg.START, username)
    # schema_validate(data, RATING_EDIT_SCHEMA_PATH)
    # logger.debug(LogMsg.SCHEMA_CHECKED)
    model_instance = db_session.query(Rating).filter(Rating.id == id).first()
    if model_instance is None:
        logger.error(LogMsg.NOT_FOUND, {'Rating_id': id})
        raise Http_error(404, Message.NOT_FOUND)
    try:
        for key, value in data.items():
            setattr(model_instance, key, value)
        edit_basic_data(model_instance, username, data.get('tags'))
        logger.debug(LogMsg.EDIT_SUCCESS, rating_to_dict(model_instance))
    except:
        logger.exception(LogMsg.EDIT_FAILED, exc_info=True)
        raise Http_error(409, Message.EDIT_FAILED)
    logger.info(LogMsg.END)
    return rating_to_dict(model_instance)


def delete(id, db_session, username):
    logger.info(LogMsg.START, username)
    model_instance = db_session.query(Rating).filter(Rating.id == id).first()
    if model_instance is None:
        logger.error(LogMsg.NOT_FOUND, {'Rating_id': id})
        raise Http_error(404, Message.NOT_FOUND)
    try:
        db_session.delete(model_instance)
        logger.debug(LogMsg.DELETE_SUCCESS, {'Rating_id': id})
    except:
        logger.exception(LogMsg.DELETE_FAILED, exc_info=True)
        raise Http_error(409, Message.DELETE_FAILED)
    logger.info(LogMsg.END)
    return Http_response(204, True)


def rating_to_dict(model):
    result = {
       'movie_id': model.movie_id ,
    'person_id':model.person_id ,
    'comment':model.comment ,
    'overall_rate':model.overall_rate,
    'novel':model.novel,
    'character':model.character ,
    'reason':model.reason ,
    'directing':model.directing ,
    'true_vision_of_enemy':model.true_vision_of_enemy,
    'iranian_life_style':model.iranian_life_style ,
    'hope':model.hope ,
    'bright_future_exposure':model.bright_future_exposure ,
    'theism':model.theism ,
    'justice_seeking':model.justice_seeking ,
    'feminism_exposure':model.feminism_exposure ,
    'individual_social_behavior':model.individual_social_behavior ,
    'family_subject':model.family_subject ,
    'alcoholic_promotion':model.alcoholic_promotion,
    'gambling_promotion':model.gambling_promotion ,
    'breaking_law_encouragement':model.breaking_law_encouragement ,
    'suicide_encouragement':model.suicide_encouragement ,
    'horror_content':model.horror_content ,
    'addiction_promotion':model.addiction_promotion ,
    'unsuitable_wearing':model.unsuitable_wearing ,
    'sexual_content':model.sexual_content ,
    'insulting_range':model.insulting_range ,
    'violence_range':model.violence_range ,
    'music':model.music,
    'sound':model.sound ,
    'visualization':model.visualization,
    'editing':model.editing ,
    'acting':model.acting ,
    'true_historiography':model.true_historiography ,
    'question_1':model.question_1 ,
    'question_2':model.question_2 ,
    'question_3':model.question_3 ,
    'question_4':model.question_4 ,
    'question_5':model.question_5 ,
    'question_6':model.question_6 ,
    'question_7':model.question_7 ,
    'question_8':model.question_8 ,
    'question_9':model.question_9 ,
    'question_10':model.question_10,
    'person':person_to_dict(model.person),
    'movie':model_to_dict(model.movie)}
    basic_attrs = model_basic_dict(model)
    result.update(basic_attrs)

    return result
