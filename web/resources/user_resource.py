from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from web.helpers import PaginationHelper
from web.models import UserSchema, User
from web.resources import AuthRequiredResource, auth
from web.status import status
from web.db import db

user_schema = UserSchema()


class UserResource(AuthRequiredResource):

    def get(self, id):
        user = User.query.get_or_404(id)
        result = user_schema.dump(user).data
        return result


class UserListResource(Resource):

    @auth.login_required
    def get(self):
        """
        Users
        Method to retrieve a single User
        ---
        tags:
          - Users
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The user Id
        responses:
          200:
            description: An User detail
            schema:
              id: User
              properties:
                id:
                  type: int
                  description: The user Id
                  default: 0
                name:
                  type: string
                  description: The user name
                  default: "User Name String"
                url:
                  type: string
                  description: The resource url that points to thisuseruser
                  default: "http://someurl.com/api/User/0"
        """ 
        pagination_helper = PaginationHelper(
            request,
            query=User.query,
            resource_for_url='api.userlistresource',
            key_name='results',
            schema=user_schema,
            order_by=User.id)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        """
        Users
        Method to create a new User
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: body
            schema:
              id: UserToUpdate
              properties:
                name:
                  type: string
                  description: The User name
                  default: "UserName"
                password:
                  type: string
                  description: The User password
                  default: "P4$sw00rd!"
        responses:
          201:
            description: The updated area
            schema:
              $ref: '#/definitions/Area'              
        """
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
        """
        Users
        Method to retrieve a single User
        ---
        tags:
          - Users
        parameters:
          - name: name
            in: path
            type: string
            required: true
            description: The user name
        responses:
          200:
            description: An User detail
            schema:
              $ref: '#/definitions/User'
        """ 
        user = User.query.filter_by(name=name).first()
        if user is None:
            response = {'message': "The user {} doesn't exists".format(name)}
            return response, status.HTTP_400_BAD_REQUEST
        result = user_schema.dump(user).data
        return result