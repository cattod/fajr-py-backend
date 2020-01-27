from .controller import add, get, get_all, delete, edit,get_by_movie
from helper import check_auth, inject_db, jsonify, pass_data, wrappers, timeit


def call_router(app):
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/ratings/<id>', 'GET', get, apply=wrappers)
    app.route('/ratings/movie/<movie_id>', 'GET', get_by_movie, apply=wrappers)

    app.route('/ratings/<id>', 'DELETE', delete, apply=[check_auth, inject_db,timeit])
    app.route('/ratings', 'POST', add, apply=data_plus_wrappers)
    app.route('/ratings/_search', 'POST', get_all, apply=data_plus_wrappers)
    app.route('/ratings/<id>', 'PUT', edit, apply=data_plus_wrappers)
