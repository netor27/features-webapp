from .status import status

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from flask_httpauth import HTTPBasicAuth
from flask import g

from .models import *
from .helpers import PaginationHelper

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


api_bp = Blueprint('api', __name__)
client_schema = ClientSchema()
area_schema = AreaSchema()
feature_schema = FeatureSchema()
user_schema = UserSchema()
api = Api(api_bp)

# User resource
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
                user.check_password_strength_and_hash_if_ok(request_dict['password'])
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


# Feature Resource
class FeatureResource(AuthRequiredResource):

    def get(self, id):
        feature = Feature.query.get_or_404(id)
        result = feature_schema.dump(feature).data
        return result


    def patch(self, id):
        feature = Feature.query.get_or_404(id)
        feature_dict = request.get_json(force=True)
        if 'title' in feature_dict:
            feature.title = feature_dict['title'] 
        if 'description' in feature_dict:
            feature.description = feature_dict['description']
        if 'target_date' in feature_dict:
            feature.target_date = feature_dict['target_date']
        if 'client_priority' in feature_dict:
            feature.client_priority = feature_dict['client_priority']    
        dumped_feature, dump_errors = feature_schema.dump(feature)
        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST
        validate_errors = feature_schema.validate(dumped_feature)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST
        try:
            feature.update()
            return self.get(id)
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = {"error": str(e)}
                return resp, status.HTTP_400_BAD_REQUEST
    
       
    def delete(self, id):
        feature = Feature.query.get_or_404(id)
        try:
            delete = feature.delete(feature)
            response = {}
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                return resp, status.HTTP_401_UNAUTHORIZED


class FeatureListResource(AuthRequiredResource):
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=Feature.query,
            resource_for_url='api.featurelistresource',
            key_name='results',
            schema=feature_schema)
        result = pagination_helper.paginate_query()
        return result


    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = feature_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST        
        try:
            # check the client and the area, if we receive values that doesn't exists, create them in the db
            client_name = request_dict['client']['name']
            client = Client.query.filter_by(name=client_name).first()
            if client is None:
                client = Client(name=client_name)
                db.session.add(client)

            area_name = request_dict['area']['name']
            area = Area.query.filter_by(name=area_name).first()
            if area is None:
                area = Area(name=area_name)
                db.session.add(area)

            feature = Feature(
                title = request_dict['title'],
                description = request_dict['description'],
                target_date= request_dict['target_date'],
                client_priority = request_dict['client_priority'],
                client = request_dict['client'],
                area = request_dict['area'])
            feature.add(feature)
            query = Feature.query.get(feature.id)
            result = feature_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


# Client Resource
class ClientResource(AuthRequiredResource):
    def get(self, id):
        client = Client.query.get_or_404(id)
        result = client_schema.dump(client).data
        return result


    def patch(self, id):
        client = Client.query.get_or_404(id)
        client_dict = request.get_json()
        if not client_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = client_schema.validate(client_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if 'name' in client_dict:
                client_name = client_dict['name'] 
                if Client.is_unique(id=id, name=client_name):
                    client.name = client_name
                else:
                    response = {'error': 'A client with the same name already exists'}
                    return response, status.HTTP_400_BAD_REQUEST
            client.update()
            return self.get(id)
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = {"error": str(e)}
                return resp, status.HTTP_400_BAD_REQUEST
       
    
    def delete(self, id):
        client = Client.query.get_or_404(id)
        try:
            client.delete(client)
            response = {}
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                return resp, status.HTTP_401_UNAUTHORIZED


class ClientListResource(AuthRequiredResource):
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=Client.query,
            resource_for_url='api.clientlistresource',
            key_name='results',
            schema=client_schema)
        result = pagination_helper.paginate_query()
        return result

    
    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = client_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        client_name = request_dict['name']
        if not Client.is_unique(id=0, name=client_name):
            response = {'error': 'A client with the same name already exists'}
            return response, status.HTTP_400_BAD_REQUEST
        try: 
            client = Client(client_name)
            client.add(client)
            query = Client.query.get(client.id)
            result = client_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}  
            return resp, status.HTTP_400_BAD_REQUEST


# Area Resource
class AreaResource(AuthRequiredResource):
    def get(self, id):
        area = Area.query.get_or_404(id)
        result = area_schema.dump(area).data
        return result


    def patch(self, id):
        area = Area.query.get_or_404(id)
        area_dict = request.get_json()
        if not area_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = area_schema.validate(area_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if 'name' in area_dict:
                area_name = area_dict['name'] 
                if Area.is_unique(id=id, name=area_name):
                    area.name = area_name
                else:
                    response = {'error': 'A area with the same name already exists'}
                    return response, status.HTTP_400_BAD_REQUEST
            area.update()
            return self.get(id)
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = {"error": str(e)}
                return resp, status.HTTP_400_BAD_REQUEST
       
    
    def delete(self, id):
        area = Area.query.get_or_404(id)
        try:
            area.delete(area)
            response = {}
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                return resp, status.HTTP_401_UNAUTHORIZED


class AreaListResource(AuthRequiredResource):
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=Area.query,
            resource_for_url='api.arealistresource',
            key_name='results',
            schema=area_schema)
        result = pagination_helper.paginate_query()
        return result


    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = area_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        area_name = request_dict['name']
        if not Area.is_unique(id=0, name=area_name):
            response = {'error': 'A area with the same name already exists'}
            return response, status.HTTP_400_BAD_REQUEST
        try: 
            area = Area(area_name)
            area.add(area)
            query = Area.query.get(area.id)
            result = area_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}  
            return resp, status.HTTP_400_BAD_REQUEST


api.add_resource(AreaListResource, '/areas/')
api.add_resource(AreaResource, '/areas/<int:id>')
api.add_resource(ClientListResource, '/clients/')
api.add_resource(ClientResource, '/clients/<int:id>')
api.add_resource(FeatureListResource, '/features/')
api.add_resource(FeatureResource, '/features/<int:id>')
api.add_resource(UserListResource, '/users/')
api.add_resource(UserResource, '/users/<int:id>')

