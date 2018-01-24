from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from web.helpers import PaginationHelper
from web.models import Client, ClientSchema
from web.resources import AuthRequiredResource
from web.status import status
from web.db import db


client_schema = ClientSchema()


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
                    response = {
                        'error': 'A client with the same name already exists'}
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
