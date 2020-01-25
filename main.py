
from bottle import Bottle, run, hook, request

from helper import generate_RID


from register.urls import call_router as register_routes
from user.urls import call_router as user_routes
from sign_up.urls import call_router as signup_routes
from app_token.urls import call_router as token_routes
from movie.urls import call_router as movie_routes
from rating.urls import call_router as rating_routes

app = Bottle()

app.catchall = False
# app = Sentry(app, sentry.sentry_client)
#
user_routes(app)
register_routes(app)
signup_routes(app)
token_routes(app)
movie_routes(app)
rating_routes(app)



app.add_hook('before_request',generate_RID)

if __name__ == '__main__':
    print('hello world')

    run(host='0.0.0.0', port=7000, debug=True, app=app)





