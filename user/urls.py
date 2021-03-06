from user.controllers.user import add as add_user, get, get_all, delete, edit,head_profile, get_profile, edit_profile, reset_pass, serach_user
from user.controllers import person
from helper import check_auth, inject_db, jsonify, pass_data, wrappers, timeit


def call_router(app):
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/users/<id>', 'GET', get, apply=wrappers)
    app.route('/users', 'GET', get_all, apply=wrappers)
    app.route('/users/<id>', 'DELETE', delete, apply=[check_auth, inject_db,timeit])
    app.route('/users', 'POST', add_user, apply=data_plus_wrappers)
    app.route('/users/_search', 'POST', serach_user, apply=data_plus_wrappers)
    app.route('/users/<id>', 'PUT', edit, apply=data_plus_wrappers)
    app.route('/users/profile', 'GET', get_profile, apply=wrappers)
    app.route('/users/profile', 'HEAD', head_profile, apply=[check_auth, inject_db,timeit])

    app.route('/profile/<id>', 'PUT', edit_profile, apply=data_plus_wrappers)
    app.route('/users/reset-password', 'POST', reset_pass, apply=[inject_db,jsonify,pass_data,timeit])


    app.route('/persons', 'POST', person.add, apply=data_plus_wrappers)
    app.route('/persons', 'GET', person.get_all, apply=wrappers)
    app.route('/persons/<id>', 'GET', person.get, apply=wrappers)
    app.route('/persons/<id>', 'PUT', person.edit, apply=data_plus_wrappers)
    app.route('/persons/<id>', 'DELETE', person.delete, apply=[check_auth, inject_db,timeit])
    app.route('/persons/_search', 'POST', person.search_person, apply=data_plus_wrappers)

