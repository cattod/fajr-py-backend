from rating.models import Rating
from repository.user_repo import check_user


def users_rated_movie_ids(username, db_session):
    user = check_user(username, db_session)
    result = db_session.query(Rating).filter(Rating.person_id == user.person_id).desc(
        Rating.creation_date).all()
    movie_ids = list()
    for item in result:
        movie_ids.append(item.movie_id)
    return movie_ids