from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource
from flask import g

from web.models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_user_password(name, password):
    user = User.query.filter_by(name=name).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


class AuthRequiredResource(Resource):
    method_decorators = [auth.login_required]
