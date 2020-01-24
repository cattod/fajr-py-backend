from .controller import add, get, get_all, delete, edit
from helper import check_auth, inject_db, jsonify, pass_data, wrappers, timeit


def call_router(app):
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/movies/<id>', 'GET', get, apply=wrappers)
    app.route('/movies/<id>', 'DELETE', delete, apply=[check_auth, inject_db,timeit])
    app.route('/movies', 'POST', add, apply=data_plus_wrappers)
    app.route('/movies/_search', 'POST', get_all, apply=data_plus_wrappers)
    app.route('/movies/<id>', 'PUT', edit, apply=data_plus_wrappers)
