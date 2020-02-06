from rating.models import Rating
from repository.user_repo import check_user


def users_rated_movie_ids(username, db_session):
    user = check_user(username, db_session)
    result = db_session.query(Rating).filter(Rating.person_id == user.person_id).all()
    movie_id_ratings = dict()
    for item in result:
        movie_id_ratings.update({item.movie_id:item.overall_rate})
    return movie_id_ratings