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
        """
        Clients
        Method to retrieve a single Client
        ---
        tags:
          - Clients
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The client Id
        responses:
          200:
            description: An Client detail
            schema:
              id: Client
              properties:
                id:
                  type: int
                  description: The client Id
                  default: 0
                name:
                  type: string
                  description: The client name
                  default: "Client Name String"
                url:
                  type: string
                  description: The resource url that points to thisclientuser
                  default: "http://someurl.com/api/Client/0"
        """    
        client = Client.query.get_or_404(id)
        result = client_schema.dump(client).data
        return result

    def patch(self, id):
        """
        Clients
        Method to update a single Client
        ---
        tags:
          - Clients
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The client Id
          - in: body
            name: body
            schema:
              id: ClientToUpdate
              properties:
                name:
                  type: string
                  description: The name of the Client
                  default: "Client Name String"
        responses:
          200:
            description: The updated client
            schema:
              $ref: '#/definitions/Client'              
        """
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
        """
        Clients
        Method to delete a single Client
        ---
        tags:
          - Clients
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The client Id
        responses:
          204:
            description: No content
        """
        client = Client.query.get_or_404(id)
        try:
            client.delete(client)
            response = {"status": status.HTTP_204_NO_CONTENT}
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class ClientListResource(AuthRequiredResource):
    def get(self):
        """
        Clients
        Method to query clients
        ---
        tags:
          - Clients
        parameters:
          - name: page
            in: path
            type: int
            required: false
            description: The page to query
          - name: size
            in: path
            type: int
            required: false
            description: The page size
        responses:
          200:
            description: An Clients list detail
            schema:
              id: ClientsList
              properties:
                results:
                  type: array
                  items: 
                    $ref: '#/definitions/Client'
                previous:
                  type: string
                  description: The resource url that points to the previous page
                  default: "http://someurl.com/api/clients/?page=1&size=5"
                next:
                  type: string
                  description: The resource url that points to the next page
                  default: "http://someurl.com/api/clients/?page=3&size=5"
                count:
                  type: int
                  description: The total count of clients in the db
                  default: 10
        """ 
        pagination_helper = PaginationHelper(
            request,
            query=Client.query,
            resource_for_url='api.clientlistresource',
            key_name='results',
            schema=client_schema,
            order_by=Client.id)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        """
        Clients
        Method to create a new Client
        ---
        tags:
          - Clients
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/ClientToUpdate'
        responses:
          201:
            description: The updated client
            schema:
              $ref: '#/definitions/Client'              
        """
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
