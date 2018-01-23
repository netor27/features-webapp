from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask_httpauth import HTTPBasicAuth

from web.helpers import PaginationHelper
from web.models import UserSchema, User
from web.resources import AuthRequiredResource, auth
from web.status import status


user_schema = UserSchema()


class UserResource(AuthRequiredResource):

    def get(self, id):
        user = User.query.get_or_404(id)
        result = user_schema.dump(user).data
        return result


class UserListResource(Resource):

    @auth.login_required
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=User.query,
            resource_for_url='api.userlistresource',
            key_name='results',
            schema=user_schema)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'user': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = user_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        name = request_dict['name']
        existing_user = User.query.filter_by(name=name).first()
        if existing_user is not None:
            response = {'user': 'An user with the same name already exists'}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            user = User(name=name)
            error_message, password_ok = \
                user.check_password_strength_and_hash_if_ok(
                    request_dict['password'])
            if password_ok:
                user.add(user)
                query = User.query.get(user.id)
                result = user_schema.dump(query).data
                return result, status.HTTP_201_CREATED
            else:
                return {"error": error_message}, status.HTTP_400_BAD_REQUEST
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


class UserLoginResource(AuthRequiredResource):

    def get(self, name):
        user = User.query.filter_by(name=name).first()
        if user is None:
            response = {'message': "The user {} doesn't exists".format(name)}
            return response, status.HTTP_400_BAD_REQUEST
        result = user_schema.dump(user).data
        return result